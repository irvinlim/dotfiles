if $(type -w complete > /dev/null); then

  # Completion for df_install
  # See http://click.palletsprojects.com/en/7.x/bashcomplete/#activation
  _df_install_completion() {
      COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                    COMP_CWORD=$COMP_CWORD \
                    _DF_INSTALL_COMPLETE=complete $1 ) )
      return 0
  }

  complete -F _df_install_completion -o default df_install;

fi
