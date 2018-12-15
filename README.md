# irvinlim's dotfiles

This repository is for storing personal configurations and automating their maintenance across multiple machines and environments.

## Features

### Installer module

The `df-install` Python command-line tool is installed, which provides multiple commands to manage configs, virtualenvs, and more.

The current subcommands include:

```sh
df-install --help
Usage: df-install [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  install-fonts
  link-configs
  setup-venv
```

### Platform-specific config symlinking

The `df-install link-configs` command is the main entrypoint to symlink all config files and directories. Rather than using another dotfile manager, I chose to write my own for flexibility in choosing how things should be symlinked.

All configs which should be symlinked can be found in `configs/`. The mapping of directories/files to their respective locations can be found in `mappings.json`.

`link-configs` distinguishes files from directories, since there may be some instances where we do not want to symlink the entire directory (such as `$HOME`), while other instances we will choose to do so (plists do not play well with symlinks as many macOS apps overwrite the symlink with a file instead).

Different platforms may also have different locations in which the config file is expected to be located in, or some apps may not be available on Linux, for example (such as iTerm2). In this case, we will specify a destination path for `darwin`, but nothing for `linux`.

### Package management

Several package managers are used to maintain a consistent environment for which apps and libraries are installed. The list of package managers include:

- Homebrew (macOS only)
- pip
- apt (Debian only, TODO)
- opam
- stack

### Virtualenv management

Since I use Python almost daily in different contexts, it makes sense to maintain separate virtualenvs that can be kept consistent across machines. As such, package management for Python modules are installed by virtualenv. See `packages/virtualenvs.json` for the configuration of virtualenvs that will be installed.

`df-install setup-venv` also helps with the installation of modules in different virtualenvs, which reads the `virtualenvs.json` configuration as well as different `requirements.txt`-like files under `packages/virtualenvs`.

Virtualenvs can be composed, meaning that for a named virtualenv, it can choose to install packages based on multiple bases. For example, we can install a `ctf` virtualenv which is based on `base`, `python2`, `tools` and `ctf`, while our pure `python2` virtualenv only uses `base`, `python2` and `tools`.

For project-specific virtualenvs, we can use `df-install setup-venv --from=base`, aliased as `ve`, which sets up a virtualenv in the current directory (named `.venv` by convention). This installs packages only from `base`. Alternatively, you wish to setup a new virtualenv from another base, specify the virtualenv name in the `--from` argument.

We can quickly switch between virtualenvs using `venv_$name`, where `$name` is the name of the global virtualenv, or local virtualenv using `venv`.

### One-time setup

My dotfile setup also extends several well-known setups, which include:

- [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)
- [Oh My Vim](https://github.com/liangxianzhe/oh-my-vim)
- [.tmux (Oh My Tmux)](https://github.com/gpakosz/.tmux)

These will be installed only once at `init.sh`.

## Installation

The following command updates config symlinks, installs/updates apps through Homebrew, and installs packages in all virtualenvs:

```sh
./setup.sh
```

This command is idempotent, meaning that we can run it several times without error.

### Initial setup

```sh
./init.sh
```

## Additional setup instructions

### iTerm2

After installing iTerm2 and running the setup script, specify the preferences location as:

```
$HOME/.iterm2
```

In addition, install the [iTerm2 shell integration](https://www.iterm2.com/documentation-shell-integration.html) as necessary.

## Exceptions

Most configuration should live in this repository, except for the following, which typically have their own method of synchronising settings in their own repository format:

- VS Code Extensions: Using [Settings Sync](https://marketplace.visualstudio.com/items?itemName=Shan.code-settings-sync), the list of extensions can be automatically synced using GitHub Gist, and (could be) automatically updated when VS Code restarts. However it also includes the VS Code settings, which would differ across environments. Maybe there should be a better way to synchronise them...
- JetBrains IDEs: Using Settings Repository, the repository is hosted elsewhere

## Repository Structure

Ideally, this repository should contain only public configuration.

For private or environment-specific configuration, maintain a downstream fork that is based on this repository and branch from `master`. The branch needs to be kept up to date with upstream manually using `git merge origin/master`. This is definitely more troublesome, so it should be avoided unless necessary (e.g. work environment contains sensitive configs).
