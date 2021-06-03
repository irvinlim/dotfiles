""""""""""""
"" VUNDLE ""
""""""""""""

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" Add plugins here!
Plugin 'editorconfig/editorconfig-vim'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

"""""""""""""""
"" OH-MY-VIM ""
"""""""""""""""

" This is the oh my vim directory
let $OH_MY_VIM=expand("$HOME/.oh-my-vim")
let &runtimepath=substitute(&runtimepath, '^', $OH_MY_VIM.",", 'g')

" Select the packages you need
let g:oh_my_vim_packages=[
            \'vim',
            \'basic',
            \'text',
            \'grep',
            \'searching',
            \'registers',
            \'navigation',
            \'files',
            \'git',
            \'python',
            \'web',
            \'tools',
            \'markdown',
            \'bookmarks',
            \'sessions',
            \'spelling',
            \'neobundle',
            \'golang'
            \]

exec ':so ' $OH_MY_VIM."/vimrc"

set mouse=a

" Disable word wrap
set formatoptions-=t
