# Add homebrew to path to load tmux on macOS
platform=$(uname)
if [[ $platform == 'Darwin' ]]; then
  # Move to back to avoid clobbering other bins from homebrew (e.g. pip)
  export PATH="$PATH:/opt/homebrew/bin"
fi

# Load RVM into a shell session *as a function*
if [[ -s "$HOME/.rvm/scripts/rvm" ]]; then source "$HOME/.rvm/scripts/rvm"; fi
