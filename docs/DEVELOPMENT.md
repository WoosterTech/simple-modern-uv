# Development

## Change Template Files

To simplify edits to project files, specifically Python files, a few things are unique about this repository:

1. All packages that would be expected in the resultant project are included as "dev" dependencies at the root level of *this* repository (see [pyproject.toml](../pyproject.toml))
1. The `template` directory is created **from** the `reference` directory, intelligently renaming files and replacing module and package names with the appropriate Jinja tags for copier to do its thing.

An important result of this is that the `template` directory should not be manually modified. Any changes to those *deliverable* files will be overwritten at the next run of `build-template`.

Therefore, all changes should be made in [reference](../reference/), where *most* type hinting will work (except for in tests?) to then be processed by the `build-template` tool into the [template](../template/) directory.

> [uv](https://docs.astral.sh/uv/getting-started/installation/) must be installed

```bash
uv run scripts/build_template.py --help
```

For more details on how the `build_template` tool works, see [build_template](./build_template.md).