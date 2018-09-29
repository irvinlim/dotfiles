export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Get the location of dotfiles directory, saved during setup.sh runs.
export DOTFILES_ROOT=`cat "$HOME/.dotfiles_root"`

##
## Set PATHs
##

# System paths
export PATH="/opt/local/bin:/opt/local/sbin:$PATH"
export PATH=$PATH:/usr/local/sbin

# Path for .local bins. Used by stack (Haskell) amongst others.
export PATH="$HOME/.local/bin:$PATH"

# CUDA
export PATH="/usr/local/cuda/bin/:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda/targets/x86_64-linux/lib:$LD_LIBRARY_PATH"

# Go
export GOPATH="$HOME/Projects"
export GOBIN="$GOPATH/bin"
export PATH="$GOBIN:$PATH"

# LaTeX
export PATH="/usr/texbin:$PATH"

# Mesos
export MESOS_NATIVE_JAVA_LIBRARY=/usr/local/Cellar/mesos/1.4.1/lib/libmesos.dylib

# GNU Core Utils
export PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH"

# Local binaries
export PATH="$HOME/bin:$PATH"

##
## Virtualenvs
##

# Evaluate and export various virtualenv paths.
export GLOBAL_VIRTUALENV_ROOT="$HOME/.virtualenvs"
export LOCAL_VIRTUALENV_PATH=".venv"
export VIRTUALENV_CONFIG_PATH="$DOTFILES_ROOT/virtualenvs.json"
export DEFAULT_VENV=`cat $VIRTUALENV_CONFIG_PATH | jq -r '.default'`
export DEFAULT_VENV_PATH="$GLOBAL_VIRTUALENV_ROOT/$DEFAULT_VENV"

# Activate default virtualenv.
[[ -e "$DEFAULT_VENV_PATH" ]] && . "$DEFAULT_VENV_PATH/bin/activate"

# Require pip to work in a virtualenv.
export PIP_REQUIRE_VIRTUALENV=true
