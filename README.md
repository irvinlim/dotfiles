# irvinlim's dotfiles

This repository is for storing personal configurations and automating the maintenance of them across multiple machines and environments.

Note that the automation component may not be fully working until I actually have to bootstrap a new macOS or Linux machine.

## Features

- Symlinking of per-platform dotfiles/configs
- Environment-specific overrides using Git forks
- Handy aliases and scripts
- One-time setup for certain apps/environments:
  - Homebrew
  - Homebrew taps/casks
  - Virtualenvs
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

## Repository Structure

Ideally, this repository should contain only public configuration.

For private or environment-specific configuration, maintain a downstream fork that is based on this repository. The fork needs to be kept up to date with upstream manually using `git merge`.
