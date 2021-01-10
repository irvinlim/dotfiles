#!/bin/bash

set -e
export PATH="$PATH:$HOME/.local/bin"

platform=$(uname)

# Ensure this script is only run on macOS.
if [[ $platform != 'Darwin' ]]; then
  echo "This script is only meant for running on macOS machines."
  exit 1
fi

# Use python -m format instead
df_install="python3 -m df_install.main"

# Set plist defaults from config file
$df_install set-macos-defaults --restart

# Set additional configs
defaults write -g ApplePressAndHoldEnabled -bool false
