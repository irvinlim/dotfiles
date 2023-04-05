#!/bin/bash

set -euo pipefail
export PIP_REQUIRE_VIRTUALENV=
export PATH="$PATH:$HOME/.local/bin"

is_gui=$(cat "$HOME/.dotfiles_gui")

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

# Install Homebrew packages
if [[ $platform == 'Darwin' ]]; then
  ./packages/homebrew/homebrew.sh
fi

# Install Go binaries
if [ ! command -v go &> /dev/null ]; then
  ./packages/go/go.sh
fi

# Install Kubernetes packages
if command -v kubectl &> /dev/null; then
  ./packages/kube/kube.sh
fi

# Set up macOS.
if [[ $platform == 'Darwin' ]]; then
  ./scripts/macos.sh
fi

# Setup virtualenvs and install packages
$df_install setup-venv --use-config

# Install VSCode extensions
if [ "$is_gui" -eq "1" ]; then
  xargs <"packages/vscode/extensions.txt" -L1 code --install-extension
fi
