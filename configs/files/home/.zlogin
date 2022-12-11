# Add homebrew to path to load tmux on macOS
platform=$(uname)
if [[ $platform == 'Darwin' ]]; then
  export PATH="/opt/homebrew/bin:$PATH"
fi

# Load RVM into a shell session *as a function*
if [[ -s "$HOME/.rvm/scripts/rvm" ]]; then source "$HOME/.rvm/scripts/rvm"; fi
