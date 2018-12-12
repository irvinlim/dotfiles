#!/bin/bash

set -e

#
# Setup script for setting up symlinks and installing applications.
# Run this script whenever new configs are added or locations are modified.
# Feel free to run this script as many times as you like, nothing should be overwritten.
#

platform=$(uname)

# Save location of dotfiles root
echo `pwd` > "$HOME/.dotfiles_root"

# Install the installer
pip install installer/ > /dev/null

# Symlink configs
df_install link_configs

# Symlink scripts folder
if [ ! -d "$HOME/scripts" ]; then
  ln -s `pwd`/scripts "$HOME"
fi

if [[ $platform == 'Darwin' ]]; then
  # Install Brew formulae
  brew bundle --file=packages/homebrew/Brewfile

  # Install casks
  brew bundle --file=packages/homebrew/Brewfile.casks

  # Upgrade all Brew packages
  brew upgrade

  # Upgrade all casks (don't use --greedy flag)
  brew cask upgrade

  # Upgrade all MAS apps
  mas upgrade
fi

# Setup virtualenvs and install packages
df_install setup_venv from_config
