#!/bin/bash

# Heavily inspired from https://github.com/nicksp/dotfiles/blob/master/setup.sh

ask_for_sudo() {

  # Ask for the administrator password upfront
  sudo -v

  # Update existing `sudo` time stamp until this script has finished
  # https://gist.github.com/cowboy/3118588
  while true; do
    sudo -n true
    sleep 60
    kill -0 "$$" || exit
  done &> /dev/null &

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

# Symlink configs
python setup/link_configs.py

# Install Homebrew
if [ ! -f /usr/local/bin/brew ]; then
  echo '### Installing Homebrew...'
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

# Install oh-my-zsh
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  echo '### Installing oh-my-zsh...'
  install_zsh
fi

# Install oh-my-vim
if [ ! -d "$HOME/.oh-my-vim" ]; then
  echo '### Installing oh-my-zsh...'
  install_vim
fi

# Install .tmux
if [ ! -d "$HOME/.tmux" ]; then
  echo '### Installing .tmux...'
  install_tmux
fi

echo 'All done!'
