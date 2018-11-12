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

# Initialisation of setup packages
pip install -r setup/requirements.txt > /dev/null

# Symlink configs
python -m setup.link_configs

# Symlink scripts folder
if [ ! -d "$HOME/scripts" ]; then
  ln -s `pwd`/scripts "$HOME"
fi

# Install Brew formulae
if [[ $platform == 'Darwin' ]]; then
  brew bundle --file=packages/homebrew/Brewfile
fi

# Casks are not automatically installed.
# Most apps are installed by hand, need to migrate them to Homebrew.
# brew bundle --file=packages/homebrew/Brewfile.casks

# Setup virtualenvs and install packages
python -m setup.setup_venv from_config
