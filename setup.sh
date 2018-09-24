#!/bin/bash

set -ex

#
# Setup script for setting up symlinks and installing applications.
# Run this script whenever new configs are added or locations are modified.
# Feel free to run this script as many times as you like, nothing should be overwritten.
# 

# Symlink configs
python setup/link_configs.py

# Install Brew formulae
brew bundle --file=homebrew/Brewfile

# Casks are not automatically installed.
# Most apps are installed by hand, need to migrate them to Homebrew.
# brew bundle --file=homebrew/Brewfile.casks
