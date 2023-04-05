platform=$(uname)

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export TERM=xterm-256color

# Get the location of dotfiles directory, saved during setup.sh runs.
export DOTFILES_ROOT=`cat "$HOME/.dotfiles_root"`

##
## Set PATHs
##

# System paths
export PATH="/opt/local/bin:/opt/local/sbin:$PATH"
export PATH=$PATH:/usr/local/sbin
export PATH=$PATH:/sbin

# Path for .local bins. Used by stack (Haskell) amongst others.
export PATH="$HOME/.local/bin:$PATH"

# Homebrew (Apple Silicon)
if [[ $platform == 'Darwin' ]]; then
  export PATH="$PATH:/opt/homebrew/bin"
fi

# CUDA
export PATH="/usr/local/cuda/bin/:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda/targets/x86_64-linux/lib:$LD_LIBRARY_PATH"

# Go
export GOPATH="$HOME/go"
export GOBIN="$GOPATH/bin"
export PATH="$GOBIN:$PATH"

# LaTeX
export PATH="/usr/texbin:/Library/TeX/texbin:$PATH"

# Mesos
export MESOS_NATIVE_JAVA_LIBRARY=/usr/local/Cellar/mesos/1.4.1/lib/libmesos.dylib

# Perl
PATH="$HOME/perl5/bin${PATH:+:${PATH}}"; export PATH;
PERL5LIB="$HOME/perl5/lib/perl5${PERL5LIB:+:${PERL5LIB}}"; export PERL5LIB;
PERL_LOCAL_LIB_ROOT="$HOME/perl5${PERL_LOCAL_LIB_ROOT:+:${PERL_LOCAL_LIB_ROOT}}"; export PERL_LOCAL_LIB_ROOT;
PERL_MB_OPT="--install_base \"$HOME/perl5\""; export PERL_MB_OPT;
PERL_MM_OPT="INSTALL_BASE=$HOME/perl5"; export PERL_MM_OPT;

# Rust
export PATH="$HOME/.cargo/bin:$PATH"

# GNU Core Utils (for macOS only)
if [[ $platform == 'Darwin' ]]; then
  export PATH="/usr/local/opt/coreutils/libexec/gnubin:/usr/local/opt/gnu-sed/libexec/gnubin:$PATH"
  export PATH="$(brew --prefix)/opt/findutils/libexec/gnubin:$PATH"
  export MANPATH="/usr/local/opt/coreutils/libexec/gnuman:$MANPATH"
fi

# Conda
export PATH="$HOME/anaconda3/bin:$PATH"

# Local binaries
export PATH="$HOME/bin:$PATH"

# Dotfile bins
export PATH="$DOTFILES_ROOT/bin:$PATH"

# Krew plugins
export PATH="${PATH}:${HOME}/.krew/bin"

##
## Virtualenvs
##

# Evaluate and export various virtualenv paths.
export GLOBAL_VIRTUALENV_ROOT="$HOME/.virtualenvs"
export LOCAL_VIRTUALENV_PATH=".venv"
export VIRTUALENV_CONFIG_PATH="$DOTFILES_ROOT/packages/virtualenvs.json"
export DEFAULT_VENV=`jq -r '.default' $VIRTUALENV_CONFIG_PATH`
export DEFAULT_VENV_PATH="$GLOBAL_VIRTUALENV_ROOT/$DEFAULT_VENV"

# Activate default virtualenv.
[[ -e "$DEFAULT_VENV_PATH" ]] && . "$DEFAULT_VENV_PATH/bin/activate"

# Require pip to work in a virtualenv.
export PIP_REQUIRE_VIRTUALENV=true

# Create aliases for each virtualenv.
while IFS='' read -r name; do
   alias venv_$name="source $GLOBAL_VIRTUALENV_ROOT/$name/bin/activate"
done < <(jq '.venvs' $VIRTUALENV_CONFIG_PATH | jq -r 'keys[]')

##
## Environment
##

export LESS='-x4 -R'
