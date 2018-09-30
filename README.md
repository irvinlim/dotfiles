# irvinlim's dotfiles

This repository is for storing personal configurations and automating their maintenance across multiple machines and environments.

## Features

- Symlinking of per-platform dotfiles/configs
- Environment-specific overrides using Git forks
- Handy aliases and scripts
- One-time setup for apps:
  - Homebrew
  - Homebrew taps/casks
- Maintenance of packages across virtualenvs
  - Composable `requirements.txt` files for syncing packages in different environments
  - Handy setup script to initialise local virtualenv using `venv`
  - Aliases to switch between global virtualenvs using `venv_$name`
- External configurations:
  - [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)
  - [Oh My Vim](https://github.com/liangxianzhe/oh-my-vim)
  - [.tmux (Oh My Tmux)](https://github.com/gpakosz/.tmux)

## Installation

The following command updates config symlinks and installs/updates apps through Homebrew:

```sh
./setup.sh
```

Ideally, the script should be able to run multiple times without affecting previous runs, and should not overwrite any existing configuration files without prior approval from the user.

The following script also sets up several one-time things, such as installation of external configs and virtualenvs:

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

## Repository Structure

Ideally, this repository should contain only public configuration.

For private or environment-specific configuration, maintain a downstream fork that is based on this repository, and branch from `master`. The branch needs to be kept up to date with upstream manually using `git merge origin/master`.
