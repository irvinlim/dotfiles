#!/bin/bash

set -ex

#
# Setup script for setting up symlinks and installing applications.
# Run this script whenever new configs are added or locations are modified.
# Feel free to run this script as many times as you like, nothing should be overwritten.
#

# Save location of dotfiles root
echo `pwd` > "$HOME/.dotfiles_root"

# Symlink configs
python setup/link_configs.py

# Symlink bin folder
if [ ! -d "$HOME/bin" ]; then
  ln -s `pwd`/bin "$HOME"
fi

# Symlink scripts folder
if [ ! -d "$HOME/scripts" ]; then
  ln -s `pwd`/scripts "$HOME"
fi

# Install Brew formulae
brew bundle --file=homebrew/Brewfile

# Casks are not automatically installed.
# Most apps are installed by hand, need to migrate them to Homebrew.
# brew bundle --file=homebrew/Brewfile.casks

# Setup virtualenvs and install packages
python setup/setup_venv.py
