# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pydantic",
#     "rich",
#     "tomli",
#     "typer",
# ]
# ///

"""When changes are made to this file, be sure to update the docs!

This script processes a source directory (default: 'reference') and generates a
template directory (default: 'template') by replacing specific placeholder values
with Jinja2 template variables. It uses the `typer` library for command-line
interface and `rich` for enhanced console output.

To update docs:

```bash
uv run typer scripts/build_template.py utils docs --output docs/build_template.md"""

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, cast, override

import typer
from rich.console import Console

if TYPE_CHECKING:
    from _typeshed import StrPath

TEXT_ENCODING: str = "utf-8"

cli = typer.Typer()
console = Console()


@dataclass
class Variable:
    text: str
    variable: str
    validators: Callable[[str], bool] | Iterable[Callable[[str], bool]] | None = None

    @override
    def __str__(self) -> str:
        return f"{{{{ {self.variable} }}}}"

    def __post_init__(self):
        if self.validators:
            if isinstance(self.validators, Iterable):
                for validator in self.validators:
                    if not validator(self.text):
                        raise ValueError(f"Validation failed for {self.variable}: {self.text}")
            elif callable(self.validators):
                if not self.validators(self.text):
                    raise ValueError(f"Validation failed for {self.variable}: {self.text}")


def email_validator(email: str) -> bool:
    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    return re.match(pattern, email) is not None


PACKAGE_NAME = Variable(
    text="PackageName", variable="package_name", validators=lambda v: v.isidentifier()
)
PACKAGE_MODULE = Variable(text="package_module", variable="package_module")
PACKAGE_DESCRIPTION = Variable(text="short description", variable="package_description")
AUTHOR_NAME = Variable(
    text="your name", variable="package_author_name", validators=lambda v: bool(v.strip())
)
AUTHOR_EMAIL = Variable(
    text="your.name@example.com", variable="package_author_email", validators=email_validator
)
PACKAGE_GITHUB_ORG = Variable(text="my-github-org", variable="package_github_org")


class JinjaPath(Path):
    """A subclass of Path that represents a path that should be converted to a Jinja template."""

    is_jinja_template: bool

    def __new__(cls, *args: "StrPath") -> "JinjaPath":
        instance = super().__new__(cls, *args)
        instance.is_jinja_template = False
        return instance

    def mark_as_jinja(self) -> None:
        self.is_jinja_template = True

    @override
    def iterdir(self):
        """Override iterdir to return JinjaPath objects with default is_jinja_template."""
        for child in super().iterdir():
            jinja_child = JinjaPath(child)
            # jinja_child.is_jinja_template is already False from __new__
            yield jinja_child

    @override
    def write_text(
        self,
        data: str,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> int:
        self = self.with_suffix(self.suffix)
        return super().write_text(data, encoding=encoding, errors=errors, newline=newline)

    @override
    def with_suffix(self, suffix: str) -> "JinjaPath":
        if self.is_jinja_template and not suffix.endswith(".jinja"):
            suffix += ".jinja"
        return cast(JinjaPath, super().with_suffix(suffix))

    @override
    def __str__(self) -> str:
        self = self.with_suffix(self.suffix)
        return super().__str__()


@dataclass
class BuildConfig:
    reference_package_name: Variable = field(default_factory=lambda: PACKAGE_NAME)
    reference_project_name: Variable = field(default_factory=lambda: PACKAGE_MODULE)
    reference_package_description: Variable = field(default_factory=lambda: PACKAGE_DESCRIPTION)
    reference_author: Variable = field(default_factory=lambda: AUTHOR_NAME)
    reference_email: Variable = field(default_factory=lambda: AUTHOR_EMAIL)
    reference_github_org: Variable = field(default_factory=lambda: PACKAGE_GITHUB_ORG)
    template_directory: Path = field(default_factory=lambda: Path("template"))

    @property
    def as_dict(self) -> dict[str, str]:
        return {
            value.text: str(value)
            for _, value in self.__dict__.items()  # pyright: ignore[reportAny]
            if isinstance(value, Variable)
        }


class Converter:
    _source_dir: Path | None = None

    def __init__(self, config: BuildConfig | None = None) -> None:
        self.config: BuildConfig = config or BuildConfig()

    @property
    def template_map(self) -> dict[str, str]:
        return self.config.as_dict

    @property
    def source_dir(self) -> Path:
        if self._source_dir is None:
            raise ValueError("Source directory is not set. Call process() first.")
        return self._source_dir

    @property
    def template_directory(self) -> Path:
        return self.config.template_directory

    def _replace_content(self, content: str) -> tuple[str, bool]:
        original_content = content
        for old_value, new_value in self.template_map.items():
            content = content.replace(old_value, new_value)
        return content, content != original_content

    def _sync_file(self, src_path: Path, dest_path: JinjaPath, *, dry_run: bool = False) -> None:
        content = src_path.read_text(encoding=TEXT_ENCODING)

        content, modified = self._replace_content(content)

        if modified:
            dest_path.mark_as_jinja()

        if not dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            _ = dest_path.write_text(content, encoding=TEXT_ENCODING)
            console.print(f"[green]Processed:[/green] {src_path} -> {dest_path}")
        else:
            console.print(f"[yellow]Dry run:[/yellow] Would write to {dest_path}")

    def _process_dir(self, dir_path: Path, *, dry_run: bool = False):
        dir_path = JinjaPath(dir_path)

        relative_dir = dir_path.relative_to(self.source_dir)

        for src_path in dir_path.iterdir():
            if src_path.is_dir():
                self._process_dir(src_path, dry_run=dry_run)
            elif src_path.is_file():
                rel_path = orig_rel_path = JinjaPath(relative_dir / src_path.name)

                for old_value, new_value in self.template_map.items():
                    rel_path_str = str(rel_path).replace(old_value, new_value)
                    rel_path = JinjaPath(rel_path_str)

                dest_path = JinjaPath(self.template_directory / rel_path)
                if rel_path.name != orig_rel_path.name:
                    dest_path.mark_as_jinja()

                self._sync_file(src_path, dest_path, dry_run=dry_run)

    def process(self, path: Path, *, dry_run: bool = False) -> None:
        if not path.exists():
            console.print(f"[red]Error: The directory {path} does not exist.[/red]")
            raise typer.Exit(code=1)

        if not path.is_dir():
            console.print(f"[red]Error: The path {path} is not a directory.[/red]")
            raise typer.Exit(code=1)

        self._source_dir = path

        self._process_dir(path, dry_run=dry_run)


def _empty_directory(directory: Path, *, dry_run: bool = False) -> None:
    if dry_run:
        console.print(f"[yellow]Dry run:[/yellow] Would empty directory {directory}")
        return
    if directory.exists() and directory.is_dir():
        for item in directory.iterdir():
            if item.is_dir():
                _empty_directory(item)
                item.rmdir()
            else:
                item.unlink()
        console.print(f"[yellow]Emptied directory:[/yellow] {directory}")


@cli.command()
def build_template(
    source_dir: Annotated[
        Path | None,
        typer.Option(
            help="The source directory to process. [default: reference]",
            file_okay=False,
            exists=True,
        ),
    ] = None,
    destination_dir: Annotated[
        Path | None,
        typer.Option(
            help="The destination directory for the processed templates. [default: template]",
            file_okay=False,
        ),
    ] = None,
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Perform a dry run without writing files.")
    ] = False,
):
    """Build the template directory from the reference directory.

    Uses a default `BuildConfig` to replace placeholder values with Jinja2 template variables.

    Defaults to processing `reference/` into `template/`.

    Currently replaces:
    - PackageName -> {{ package_name }}
    - package_module -> {{ package_module }}
    - short description -> {{ package_description }}
    - your name -> {{ package_author_name }}
    - your.email@example.com -> {{ package_author_email }}
    """
    source_dir = source_dir or Path("reference")

    console_prefix = "[dry run] " if dry_run else ""

    if not destination_dir:
        config = BuildConfig()
    else:
        config = BuildConfig(template_directory=destination_dir)

    destination_dir = config.template_directory

    if destination_dir.exists():
        console.print(f"[yellow]Warning: The directory {destination_dir} already exists.[/yellow]")
        if not typer.confirm("Do you want to continue and overwrite its contents?"):
            console.print("[red]Operation cancelled by user.[/red]")
            raise typer.Exit(code=1)
        _empty_directory(destination_dir, dry_run=dry_run)

    console.rule(
        f"{console_prefix}Building templates from [green]{source_dir}[/green] to [blue]{destination_dir}[/blue]"
    )

    converter = Converter(config=config)

    console.print(f"{console_prefix}[magenta]Starting processing...[/magenta]")

    converter.process(source_dir, dry_run=dry_run)

    console.rule(f"[blue]{console_prefix}Output directory:[/blue] {destination_dir}")


if __name__ == "__main__":
    cli()
