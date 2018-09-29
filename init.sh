#!/bin/bash

set -e

#
# First-time init script.
# There should be no need to run this script once a machine has been initialised,
# although it should not overwrite anything. However to speed things up, we can
# safely omit these steps when updating configs across machines.
#
# Heavily inspired from https://github.com/nicksp/dotfiles/blob/master/setup.sh
#

install_homebrew() {
  platform=$(uname)

  if [[ $platform == 'Darwin' ]]; then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  fi
}

install_zsh () {
  # Test to see if zshell is installed.  If it is:
  if [ -f /bin/zsh -o -f /usr/bin/zsh ]; then
    # Install Oh My Zsh if it isn't already present
    if [[ ! -d $dir/oh-my-zsh/ ]]; then
      sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
    fi
    # Set the default shell to zsh if it isn't currently set to zsh
    if [[ ! $(echo $SHELL) == $(which zsh) ]]; then
      chsh -s $(which zsh)
    fi
  else
    # If zsh isn't installed, get the platform of the current machine
    platform=$(uname);
    # If the platform is Linux, try an apt-get to install zsh and then recurse
    if [[ $platform == 'Linux' ]]; then
      if [[ -f /etc/redhat-release ]]; then
        sudo yum install zsh
        install_zsh
      fi
      if [[ -f /etc/debian_version ]]; then
        sudo apt-get install zsh
        install_zsh
      fi
    # If the platform is OS X, tell the user to install zsh :)
    elif [[ $platform == 'Darwin' ]]; then
      echo "We'll install zsh, then re-run this script!"
      brew install zsh
      exit
    fi
  fi
}

install_vim() {
  # Check if oh-my-vim is already present
  if [ -d "$HOME/.oh-my-vim" ]; then
    exit
  fi

  # Perform installation instructions here:
  # https://github.com/liangxianzhe/oh-my-vim

  platform=$(uname)

  if [[ $platform == 'Darwin' ]]; then
    # Install dependencies for macOS
    curl -sL https://raw.github.com/liangxianzhe/oh-my-vim/master/tools/prepare_mac.sh | sh

    # Install oh-my-vim
    curl -sL https://raw.github.com/liangxianzhe/oh-my-vim/master/tools/install.sh | sh
  elif [[ $platform == 'Linux' ]]; then
    echo 'Installation for dependencies for oh-my-vim on Linux is not available, you have to install dependencies yourself.'
    echo 'For more information, see https://github.com/liangxianzhe/oh-my-vim'

    # Install oh-my-vim
    curl -sL https://raw.github.com/liangxianzhe/oh-my-vim/master/tools/install.sh | sh
  fi
}

install_tmux() {
  # See https://github.com/gpakosz/.tmux
  git clone https://github.com/gpakosz/.tmux.git ~/.tmux
  ln -sf .tmux/.tmux.conf ~/.tmux.conf
}

# Install Homebrew
if [ ! -f /usr/local/bin/brew ]; then
  echo -e '\033[0;33mInstalling Homebrew...\033[0m'
  install_homebrew
fi

# Install oh-my-zsh
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  echo -e '\033[0;33mInstalling oh-my-zsh...\033[0m'
  install_zsh
fi

# Install oh-my-vim
if [ ! -d "$HOME/.oh-my-vim" ]; then
  echo -e '\033[0;33mInstalling oh-my-vim...\033[0m'
  install_vim
fi

# Install .tmux
if [ ! -d "$HOME/.tmux" ]; then
  echo -e '\033[0;33mInstalling .tmux...\033[0m'
  install_tmux
fi

# Install nvm
if [ ! -d "$HOME/.nvm" ]; then
  echo -e '\033[0;33mInstalling nvm...\033[0m'
  curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
fi

echo -e '\033[0;32mFirst time installation is complete.\033[0m'
