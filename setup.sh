#!/bin/bash

set -e
export PIP_REQUIRE_VIRTUALENV=

#
# Setup script for setting up symlinks and installing applications.
# Run this script whenever new configs are added or locations are modified.
# Feel free to run this script as many times as you like, nothing should be overwritten.
#

platform=$(uname)

# Save location of dotfiles root
echo `pwd` > "$HOME/.dotfiles_root"

# Install the installer
echo -e '\033[0;33mSetting up df-install.\033[0m'
/usr/local/bin/pip3 install -U pip
/usr/local/bin/pip3 install installer/

# Export any env vars required from .profile when it doesn't exist yet.
export DOTFILES_ROOT=`cat "$HOME/.dotfiles_root"`

# Symlink configs
/usr/local/bin/df-install link-configs

# Symlink scripts folder
if [ ! -d "$HOME/scripts" ]; then
  ln -s `pwd`/scripts "$HOME"
fi

if [[ $platform == 'Darwin' ]]; then
  if [ -f "$DOTFILES_ROOT/.brewfiles" ]; then
    # Use .brewfiles to determine formulae files
    cat "$DOTFILES_ROOT/.brewfiles" | xargs -I {} brew bundle --file=packages/homebrew/{}
  else
    # Install hardcoded formulae
    brew bundle --file=packages/homebrew/Brewfile
    brew bundle --file=packages/homebrew/Brewfile.casks
    brew bundle --file=packages/homebrew/Brewfile.mas
  fi

  # Upgrade all Brew packages
  brew upgrade

  # Upgrade all casks (don't use --greedy flag)
  brew cask upgrade

  # Upgrade all MAS apps
  mas upgrade
fi

# Setup virtualenvs and install packages
/usr/local/bin/df-install setup-venv --from-config
