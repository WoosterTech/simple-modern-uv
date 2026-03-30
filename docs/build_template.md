# `build-template`

Build the template directory from the reference directory.

Uses a default `BuildConfig` to replace placeholder values with Jinja2 template variables.

Defaults to processing `reference/` into `template/`.

Currently replaces:
- PackageName → {{ package_name }}
- package_module → {{ package_module }}
- short description → {{ package_description }}
- your name → {{ package_author_name }}
- your.email@example.com → {{ package_author_email }}

**Usage**:

```console
$ build-template [OPTIONS]
```

**Options**:

* `--source-dir DIRECTORY`: The source directory to process.
* `--destination-dir DIRECTORY`: The destination directory for the processed templates.
* `--dry-run`: Perform a dry run without writing files.
* `-q, --quiet`: Suppress prompts. Will force creation without asking for permission.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.
