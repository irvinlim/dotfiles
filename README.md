# irvinlim's dotfiles

This repository is for storing personal configurations and automating their maintenance across multiple machines and environments.

## Features

- Symlinking of per-platform dotfiles/configs
- Handy aliases and scripts
- Synchronisation of apps through:
  - macOS: Homebrew taps + casks
  - Debian: apt (_TODO_)
- Maintenance of installed packages across virtualenvs
  - Composable `requirements.txt` files for syncing packages in different virtualenvs
  - Handy setup script to initialise local virtualenv using `ve`
  - Aliases to switch between global virtualenvs using `venv_$name`, or local virtualenv using `venv`
- External configurations:
  - [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)
  - [Oh My Vim](https://github.com/liangxianzhe/oh-my-vim)
  - [.tmux (Oh My Tmux)](https://github.com/gpakosz/.tmux)

## Installation

The following command updates config symlinks, installs/updates apps through Homebrew, and installs packages in all virtualenvs:

```sh
./setup.sh
```

Ideally, the script should be able to run multiple times without affecting previous runs, and should not overwrite any existing configuration files without prior approval from the user.

The following script also sets up several one-time things, such as first-time installation of tools and external configs:

```sh
./init.sh
```

Note that `init.sh` may not be fully working until I actually have to bootstrap a new macOS or Linux machine.

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
