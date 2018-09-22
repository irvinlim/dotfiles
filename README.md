# irvinlim's dotfiles

This repository is for storing personal configurations and automating the maintenance of them across multiple machines and environments.

## Installation

The following command creates the symlinks of dotfiles to the necessary locations, such as `$HOME`:

```sh
./setup.sh
```

The script also sets up several one-time things, such as installation of apps and virtualenvs. Ideally, the script should be able to run multiple times without affecting previous runs, and should not overwrite any existing configuration files without prior approval from the user.

## Repository Structure

Ideally, this repository should contain only public configuration.

For private or environment-specific configuration, maintain a downstream fork that is based on this repository. The fork needs to be kept up to date with upstream manually using `git merge`.
