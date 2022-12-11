#!/bin/bash

set -e
export PIP_REQUIRE_VIRTUALENV=

# Add Python bin PATH temporarily
export PATH="$PATH:$HOME/.local/bin"

# Add Homebrew bin PATH temporarily
export PATH="$PATH:/opt/homebrew/bin"

# Use python -m format instead
pip3="python3 -m pip"
df_install="python3 -m df_install.main"

#
# First-time init script.
# There should be no need to run this script once a machine has been initialised,
# although it should not overwrite anything. However to speed things up, we can
# safely omit these steps when updating configs across machines.
#
# Heavily inspired from https://github.com/nicksp/dotfiles/blob/master/setup.sh
#
# NOTE: This script only supports Ubuntu for Linux!

install_homebrew() {
  platform=$(uname)

  if [[ $platform == 'Darwin' ]]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
}

install_zsh () {
  # Test to see if zshell is installed.  If it is:
  if [ -f /bin/zsh -o -f /usr/bin/zsh ]; then
    # Install Oh My Zsh if it isn't already present
    if [[ ! -d $dir/oh-my-zsh/ ]]; then
      sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sed '/\s*env\s\s*zsh\s*/d')"
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
        sudo apt-get -y install zsh
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
  platform=$(uname)

  # Install vim
  if ! command -v vim &> /dev/null; then
    if [[ $platform == 'Linux' ]]; then
      echo -e '\033[0;33mInstalling vim...\033[0m'
      sudo apt-get -y install vim
    elif [[ $platform == 'Darwin' ]]; then
      echo -e '\033[0;33mInstalling vim...\033[0m'
      brew install vim
    fi
  fi

  # Install Vundle
  if [ ! -d "$HOME/.vim/bundle/Vundle.vim" ]; then
    echo -e '\033[0;33mInstalling Vundle...\033[0m'
    git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
  fi

  # Install oh-my-vim: https://github.com/liangxianzhe/oh-my-vim
  if [ ! -d "$HOME/.oh-my-vim" ]; then
    echo -e '\033[0;33mInstalling .oh-my-vim...\033[0m'

    if [[ $platform == 'Darwin' ]]; then
      # Install dependencies for macOS
      brew install ctags ag ack ranger tig lua luajit
    elif [[ $platform == 'Linux' ]]; then
      echo 'Installation for dependencies for oh-my-vim on Linux is not available, you have to install dependencies yourself.'
      echo 'For more information, see https://github.com/liangxianzhe/oh-my-vim'
    fi

    # Install oh-my-vim
    curl -sL https://raw.github.com/liangxianzhe/oh-my-vim/master/tools/install.sh | sh
  fi
}

install_tmux() {
  platform=$(uname)

  # Install tmux itself
  if [[ $platform == 'Linux' ]]; then
    sudo apt-get -y install tmux
  elif [[ $platform == 'Darwin' ]]; then
    brew install tmux
  fi

  # Install .tmux
  if [ ! -d "$HOME/.tmux" ]; then
    echo -e '\033[0;33mInstalling .tmux...\033[0m'

    # See https://github.com/gpakosz/.tmux
    git clone https://github.com/gpakosz/.tmux.git ~/.tmux
    ln -sf .tmux/.tmux.conf ~/.tmux.conf
  fi

  # Install tpm
  if [ ! -d "$HOME/.tmux/plugins/tpm" ]; then
    mkdir -p ~/.tmux/plugins
    git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
    tmux source ~/.tmux.conf
    ~/.tmux/plugins/tpm/bin/install_plugins
  fi
}

ensure_python() {
  platform=$(uname)

  mkdir -p "$HOME/.virtualenvs"

  if [[ $platform == "Linux" ]]; then
    sudo apt-get install -y python3-pip
    $pip3 install virtualenv
  elif [[ $platform == "Darwin" ]]; then
    brew install python 2> /dev/null

    # Rewrite the path to python3 here, because otherwise we will be using the system default.
    pip3="/opt/homebrew/bin/python3 -m pip"
    df_install="/opt/homebrew/bin/python3 -m df_install.main"

    curl https://bootstrap.pypa.io/get-pip.py -sSL | python3
    $pip3 install virtualenv
  fi
}

#########

# Start here!

# Create .dotfiles_root if it doesn't exist.
if [ ! -f "$HOME/.dotfiles_root" ]; then
  echo `pwd` > "$HOME/.dotfiles_root"
fi

# Ask if this environment is a GUI environment, which can skip installation of graphical tools and other stuff.
if [ ! -f "$HOME/.dotfiles_gui" ]; then
  echo -n "[?] Does this environment have a GUI? This would skip installation of graphical tools as necessary: "
  read -n 1 is_gui
  echo

  if [[ "$is_gui" == "n" ]]; then
    echo "0" > "$HOME/.dotfiles_gui"
  else
    echo "1" > "$HOME/.dotfiles_gui"
  fi
fi

is_gui=`cat "$HOME/.dotfiles_gui"`
platform=$(uname)

# Install dependencies for Linux
if [[ $platform == 'Linux' ]]; then
  sudo apt-get update

  DEPS="curl git jq python3-pip language-pack-en"
  sudo apt-get -y install $DEPS
fi

# Install Homebrew
if [[ $platform == 'Darwin' && ! -f /usr/local/bin/brew ]]; then
  echo -e '\033[0;33mInstalling Homebrew...\033[0m'
  install_homebrew
fi

# Install oh-my-zsh
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  echo -e '\033[0;33mInstalling oh-my-zsh...\033[0m'
  install_zsh
fi

# Install vim stuff
install_vim

# Install tmux stuff
install_tmux

# Install nvm
if [ ! -d "$HOME/.nvm" ]; then
  echo -e '\033[0;33mInstalling nvm...\033[0m'
  curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
fi

# Ensure Python installation is alright
# Installs pip and virtualenv
echo -e '\033[0;33mEnsuring Python installation is valid...\033[0m'
ensure_python

# Initialisation of setup packages
$pip3 install -r installer/requirements.txt

# Install the installer
echo -e '\033[0;33mSetting up df-install.\033[0m'
$pip3 install installer/

# Install fonts
if [ "$is_gui" -eq "1" ]; then
  # Install fonts
  echo -e '\033[0;33mRunning df-install install-fonts.\033[0m'
  DOTFILES_ROOT=`cat "$HOME/.dotfiles_root"` $df_install install-fonts
fi

echo -e '\033[0;32mFirst time installation is complete.\033[0m'
