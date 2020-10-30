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
  homebrew_root="${DOTFILES_ROOT}/packages/homebrew"

  # Use .brewfiles to determine formulae files
  brewfiles="${DOTFILES_ROOT}/.brewfiles"
  if [ ! -f "${brewfiles}" ]; then
    echo > "${brewfiles}"
    echo Brewfile >> "${brewfiles}"
    echo Brewfile.casks >> "${brewfiles}"
  fi

  # Concat all brewfiles
  brewfile="${homebrew_root}/.brewfile.cat"
  cat "${brewfiles}" | xargs -I % cat "${homebrew_root}/%" > "${brewfile}"

  # Install from brewfile
  brew bundle --file="${brewfile}"

  # Clean up
  rm "${brewfile}"

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

# Set up macOS.
if [[ $platform == 'Darwin' ]]; then
  ./scripts/macos.sh
fi

# Setup virtualenvs and install packages
$df_install setup-venv --use-config
