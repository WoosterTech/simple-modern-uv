# `build-template`

Build the template directory from the reference directory.

Uses a default `BuildConfig` to replace placeholder values with Jinja2 template variables.

Defaults to processing `reference/` into `template/`.

Currently replaces:
- PackageName -&gt; {{ package_name }}
- package_module -&gt; {{ package_module }}
- short description -&gt; {{ package_description }}
- your name -&gt; {{ package_author_name }}
- your.email@example.com -&gt; {{ package_author_email }}

**Usage**:

```console
$ build-template [OPTIONS]
```

**Options**:

* `--source-dir DIRECTORY`: The source directory to process.
* `--destination-dir DIRECTORY`: The destination directory for the processed templates.
* `--dry-run`: Perform a dry run without writing files.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.
