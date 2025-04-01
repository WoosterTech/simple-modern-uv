[![As usual, XKCD has a comic for
this](https://imgs.xkcd.com/comics/python_environment.png)](https://xkcd.com/1987/)

(As usual, XKCD has a comic for this.
Appropriately enough, the comic is out of date.)

# simple-modern-uv

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-border.json)](https://github.com/copier-org/copier)
[![X (formerly Twitter)
Follow](https://img.shields.io/twitter/follow/ojoshe)](https://x.com/ojoshe)

## What is This?

**simple-modern-uv** is a minimal, modern **Python project template** for new projects
(Python 3.10–3.13) based on [**uv**](https://docs.astral.sh/uv/). This template aims to
be a good base for serious work but also simple so it's an easy option for any small
project, like an open source library or tool.

> [!TIP]
> 
> **In a hurry?**
> 
> You can use this template right from your terminal.
> Try running:
> 
> ```
> uvx uvinit
> ```
> 
> The [uvinit](https://jlevy/uvinit) tool now walks you through using this template.
> 
> For more installation options, scroll down to [How to Use This
> Template](#how-to-use-this-template).

## Why a New Python Project Template?

> **The Story So Far**
> 
> In the beginning, there was a hack called
> [`setup.py`](https://github.com/pypa/setuptools) for packaging (1990s–2000s) and it
> was not good.
> 
> Then there arose [`virtualenv`](https://github.com/pypa/virtualenv),
> [`pip`](https://github.com/pypa/pip), and `requirements.txt` for isolated environments
> (2008–2011). Yet confusion still reigned.
> 
> Meanwhile, [`conda`](https://github.com/conda/conda),
> [`pyenv`](https://github.com/pyenv/pyenv), [`brew`](https://github.com/Homebrew/brew),
> and [`PyInstaller`](https://github.com/pyinstaller/pyinstaller) vied to rule the
> system installations (2010s).
> 
> Years of dissatisfaction led to the spread of a new religion,
> [`pyproject.toml`](https://github.com/pypa/pyproject.toml).
> Adherents of [`poetry`](https://github.com/python-poetry/poetry),
> [`pipenv`](https://github.com/pypa/pipenv), and [`pipx`](https://github.com/pypa/pipx)
> promised peace and prosperity (2020s) yet somehow, life felt mostly the same.
> 
> Then AI robots began to invade.
> Rebel forces [`uv`](https://github.com/astral-sh/uv) and
> [`pixi`](https://github.com/prefix-dev/pixi) aligned with Rust gathered strength …

Apologies for the digression.
The point is that unfortunately, the accidents of history make it quite confusing to
learn best practices for setting up Python projects and dependencies.
But it shouldn't have to be this difficult, especially since uv has now significantly
simplified Python dev tooling.

I think a good project template should be **3 Ms: minimalist, modern, and maintained**.
I looked at [other templates](#alternatives) but wanted one that was modern and "done
right" but *absolutely as simple as possible*. Few existing templates seem to be both
simple and use the newest generation of tools and best practices.

If you haven't switched to uv, I can say I too was a little hesitant.
It's often possible to switch dev tooling prematurely because a the new tool is shiny
and exciting. But the advantages of uv have become too numerous to ignore.

This is the template I now use myself as I have been migrating from Poetry to uv for
several projects. It's new but it's working well.

The template is short enough to read and understand in about 10 minutes.
It's **only ~300 lines of code** so you can just look at it, use it, and change what you
want without fuss.

Because this template is minimal, you can always start with it and then pull in other
tools and features if you want them.

## Why Use a Copier Template?

One other benefit of this template is it uses
[**copier**](https://github.com/copier-org/copier).

Unlike many previous project template tools, it has you can
[pull future changes](#updating-your-project-template) to this template back into your
project any time.

You can start a project now, then if this template improves or is updated with other
tools, you can pull those improvements back into your project, much like a git merge.
You could even fork this repo yourself, then build your own forked template, and
maintain it yourself.

> [!NOTE]
> 
> If you're not familiar with copier, take a moment to understand the
> [update feature](#updating-your-project-template).
> Then the options below will make sense.
> I put a few more thoughts on why a workflow like this is underrated is in
> [this thread](https://x.com/ojoshe/status/1896696860297019733).

## What Tools are In This Template?

simple-modern-uv uses uses the tools I've come to think are best for new projects:

- [**uv**](https://github.com/astral-sh/uv) for project setup and dependencies.
  There is also a simple makefile for dev workflows, but it simply is a convenience for
  running uv commands.

- [**ruff**](https://github.com/charliermarsh/ruff) for modern linting and formatting.
  Previously, [black](https://github.com/psf/black) was the definitive formatting tool,
  but ruff now handles linting and fast, black-compatible formatting.

- [**GitHub Actions**](https://github.com/actions/setup-python) for CI and publishing
  workflows.

- [**Dynamic versioning**](https://github.com/ninoseki/uv-dynamic-versioning/) so
  release and package publication is as simple as creating a tag/release on GitHub (no
  machinery needed to manually bump versions and commit files every release).

- Workflows for **packaging and publishing to PyPI** with uv.
  This has always been more confusing than it should be.
  The
  [official docs](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
  about packaging are several pages long, and then even
  [toy tutorials](https://realpython.com/pypi-publish-python-package/) about publishing
  are even longer. This template makes all of that basically automatic with uv, GitHub
  Actions, and dynamic versioning.

- Type checking with [**BasedPyright**](https://github.com/detachhead/basedpyright).
  (See below for more on this.)

- [**Pytest**](https://github.com/pytest-dev/pytest) for tests.

- [**codespell**](https://github.com/codespell-project/codespell) for drop-in spell
  checking.

- **Starter docs** you can include if you wish for users
  ([README.md](https://github.com/jlevy/simple-modern-uv/blob/main/template/README.md.jinja))
  and developers
  ([development.md](https://github.com/jlevy/simple-modern-uv/blob/main/template/development.md.jinja)).
  It helps to keep these docs and reminders on uv Python setup/installation, basic dev
  workflows, and VSCode extensions in the template itself so they are up to date.

## What's the Best Python Type Checker?

The choice of what tool to use for type checking deserves some explanation.
This seems to be a confusing area.

Like many, I'd previously been using [Mypy](https://github.com/python/mypy), the OG type
checker for Python. Mypy has since been enhanced with
[BasedMypy](https://github.com/KotlinIsland/basedmypy).

The other popular alternative is Microsoft's
[Pyright](https://github.com/microsoft/pyright).
And it has a newer extension and fork called
[BasedPyright](https://github.com/DetachHead/basedpyright).

All of these work in build systems.
But this is a choice not just of build tooling—it is far preferable to have your type
checker warnings align with your IDE warnings.
With the rises of AI-powered IDEs like Cursor and Windsurf that are VSCode extensions,
it seems like type checking support as a VSCode-compatible extension is essential.

However, Microsoft's popular
[Mypy VSCode extension](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)
is licensed only for use in VSCode (not other IDEs) and
[sometimes](https://forum.cursor.com/t/pylance-server-fails-to-initialize-due-to-licensing-restriction/48548)
[refuses](https://forum.cursor.com/t/does-pylance-just-not-work-with-cursor-how-to-get-imports-in-quick-fix-menu/5747)
to work in Cursor. [Cursor's docs](https://docs.cursor.com/guides/languages/python)
suggest Mypy but don't suggest a VSCode extension.

After some experimentation, I found
[BasedPyright](https://github.com/detachhead/basedpyright) to be a credible improvement
on [Pyright](https://github.com/microsoft/pyright).
BasedPyright is well maintained, is faster than Mypy, and has a good
[VSCode extension](https://marketplace.visualstudio.com/items?itemName=detachhead.basedpyright)
that works with Cursor and other VSCode forks.
So I have now switched this template to use BasedPyright.
(But please drop a note in the Discussion tab if you have better suggestions.)

## What Does This Template Not Include?

The template doesn't have lots of options or try to use every bell and whistle.
It just adds the above essentials.

This template **does not** handle:

- Using Docker

- Building websites or docs, e.g. with [mkdocs](https://github.com/mkdocs/mkdocs)

- Using [Conda](https://github.com/conda/conda) for dependencies (but note many deep
  learning libraries like PyTorch now support pip so this isn't as necessary as often as
  it used to be)

- Using a code repo or build system that isn't GitHub and GitHub Actions

- Boilerplate docs or project management of any kind, like issue templates, contributing
  guidelines, code of conduct, etc.

If you want them, just add these yourself.
:) Also see [below](#alternatives) for other templates you can look at or use as
references.

## How to Use This Template

> [!NOTE]
> 
> By default this template uses MIT license.
> If you want a different license or are not publishing your project as open source,
> update `license` in pyproject.yaml and the LICENSE file.
> If desired, you may delete the `.github/workflows/publish.yml` file if you are not
> publishing to PyPI.

The template can be used in three ways.
Option 1 is the quickest option with full flexibility.
Option 2 is the normal way to use a copier template by hand.
Option 3 is handy if you prefer a GitHub template.

### Option 1: Run `uvx uvinit`

I've now created a little tool, [uvinit](https://www.github.com/jlevy/uvinit) that
copies this template for you.

It's basically the same as running `copier` and a few `git` commands yourself, with a
little more guidance and less typing.

### Option 3: Use `copier` and `git` Yourself

This template uses [copier](https://github.com/copier-org/copier), which seems like the
best tool nowadays for project templates.
Using copier is the recommended approach since it then lets you instantiate the template
variables and makes future updates possible.
But it requires a few more commands.

To create a new project repo with `copier`:

```shell
# Install copier:
uv tool install copier

# Change dirs to the place you want the new GitHub repo to be.
cd ~/projects/github   # Wherever you do your project work.

# Clone this template. This does everything!
# It will fetch from this GitHub repo and create a new directory
# with whatever name you put below:
copier copy gh:jlevy/simple-modern-uv YOURNEWREPO
# Then follow the instructions.
```

You can enter names for the project, description, etc., or just press enter and later
look for `changeme` in the code.

Once you have the template set up, you will need to check the code into Git for uv to
work. [Create a new GitHub
repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
and add your initial code:

```shell
cd PROJECT
git init
# Make license or other initial adjustments if needed.
git add .
git commit -m "Initial commit from simple-modern-uv."
# Create repo on GitHub.
git remote add origin git@github.com:OWNER/PROJECT.git  # or https://github.com/...
git branch -M main
git push -u origin main
```

### Option 3: Use the GitHub Template

If you prefer you can click the **use this template** on
[**this repository**](https://github.com/jlevy/simple-modern-uv-template), which is the
current output of this template.

Go there and hit the "Use this template" button.
Once you have the code, search for **`changeme`** for all field names like project name,
author, etc. You want to do this to the `.copier-answers.yml` file as well.
You will also want to check the license/copyright.

## Getting Started on Your Project

In the template project itself, the
[**default readme**](https://github.com/jlevy/simple-modern-uv) and the file
[**development.md**](https://github.com/jlevy/simple-modern-uv/blob/main/template/development.md.jinja)
cover the install and build workflows, as well as links to IDE extensions.
See
[**publishing.md**](https://github.com/jlevy/simple-modern-uv/blob/main/template/publishing.md)
for publishing to PyPI. You'll find all these in your project directory, too.

## Updating Your Project Template

If you use Option 2 or if you pick Option 1 and correctly fill in your
`.copier-answers.yml` file, you have the option to update your project with any future
updates to this template at any time.

If this file is updated with your project name etc., then you can
[update your project](https://copier.readthedocs.io/en/latest/updating/) to reflect any
changes to this template by running `copier update`.

## Alternatives

[Poetry](https://python-poetry.org/docs/basic-usage/) is a good option for managing
dependencies and is not as new as uv and arguably more mature (it just hit version 2.0).
This template is based on my earlier Poetry template,
[simple-modern-poetry](https://github.com/jlevy/simple-modern-poetry).

A great resource to check is
[**python-blueprint**](https://github.com/johnthagen/python-blueprint), which is a more
established template with an excellent overview of other standard Python project best
practices. It uses [Poetry](https://python-poetry.org/docs/basic-usage/),
[nox](https://github.com/wntrblm/nox),
[Material for Mkdocs](https://github.com/squidfunk/mkdocs-material), and Docker.

For [Conda](https://github.com/conda/conda) dependencies, also consider the newer
[**pixi**](https://github.com/prefix-dev/pixi/) package manager.

Finally, there are several other good uv templates, such as
[**cookiecutter-uv**](https://github.com/fpgmaas/cookiecutter-uv) and
[**copier-uv**](https://github.com/pawamoy/copier-uv) you may wish to consider.

This template takes a somewhat different philosophy.
I found existing templates to have machinery or files you often don't need.
And it's hard to maintain a complex template repo.
This is intended instead to be a very simple template.
You can always add to it if you want.

## Contributing

I'm new to uv, so please help me improve this!
Please use the Discussions thread with any feedback or suggestions.
PRs welcome on [this repository](https://github.com/jlevy/simple-modern-uv) (not on the
GitHub template repo, which mirrors this one).
