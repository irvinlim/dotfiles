#!/bin/bash

set -e
export PIP_REQUIRE_VIRTUALENV=
export PATH="$PATH:$HOME/.local/bin"

# Use python -m format instead
pip3="python3 -m pip"
df_install="python3 -m df_install.main"

#
# Setup script for setting up symlinks and installing applications.
# Run this script whenever new configs are added or locations are modified.
# Feel free to run this script as many times as you like, nothing should be overwritten.
#

# Ask for the administrator password upfront
sudo -v

# Keep-alive sudo
# Inspired from mathiasbynens/dotfiles
while true; do
  sudo -n true
  sleep 60
  kill -0 "$$" || exit
done 2>/dev/null &

platform=$(uname)
DOTFILES_ROOT=$(cat "$HOME/.dotfiles_root")

# Save location of dotfiles root
pwd >"$HOME/.dotfiles_root"

# Install the installer
echo -e '\033[0;33mSetting up df-install.\033[0m'
$pip3 install installer/

# Export any env vars required from .profile when it doesn't exist yet.
export DOTFILES_ROOT

# Symlink configs
$df_install link-configs

# Install Vundle plugins
vim +PluginInstall +qall

# Symlink scripts folder
if [ ! -d "$HOME/scripts" ]; then
  ln -s "$(pwd)/scripts" "$HOME"
fi

if [[ $platform == 'Darwin' ]]; then
  # Use .brewfiles to determine formulae files
  brewfiles="${DOTFILES_ROOT}/.brewfiles"
  if [ -f "${brewfiles}" ]; then
    xargs <"${brewfiles}" -I % brew bundle --file=packages/homebrew/%
  else
    # Install hardcoded formulae
    brew bundle --file=packages/homebrew/Brewfile
    brew bundle --file=packages/homebrew/Brewfile.casks
  fi

  # Upgrade all Brew packages
  brew upgrade -n
  read -rp 'Continue? [y/N] ' -n1 ans
  echo -en '\n'
  if [[ $ans == 'y' ]]; then
    brew upgrade
  fi

  # Upgrade all casks (don't use --greedy flag)
  brew cask upgrade

  # Upgrade all MAS apps
  mas upgrade
fi

# Use gobin to install go binaries
if [[ -n $GOPATH ]]; then
  ./packages/go/gobin.sh
fi

# Set up plist defaults.
if [[ $platform == 'Darwin' ]]; then
  $df_install set-macos-defaults --restart
fi

# Setup virtualenvs and install packages
$df_install setup-venv --use-config
