#!/bin/bash

platform=$(uname)

if [[ $platform == "Linux" ]]; then
  sudo apt-get install -y python3-pip
  sudo pip3 install virtualenv 
elif [[ $platform == "Darwin" ]]; then
  brew install python
  sudo easy_install pip
fi

if [ ! -d "$HOME/.virtualenvs/python3.6" ]; then
  virtualenv -p python3 "$HOME/.virtualenvs/python3.6"
fi
