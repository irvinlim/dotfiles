#!/bin/sh

set -euo pipefail

##
## Helper script to install Homebrew packages using brewfiles.
##

if [[ -z "${DOTFILES_ROOT}" ]]; then
  echo "Error: DOTFILES_ROOT not defined"
  exit 1
fi

platform=$(uname)
package_root="${DOTFILES_ROOT}/packages/homebrew"
package_lists="${DOTFILES_ROOT}/.packages-homebrew"

# Skip if current platform is not macOS.
if [[ $platform != 'Darwin' ]]; then
  exit
fi

# Generate default package list if not present
if [ ! -f "${package_lists}" ]; then
  touch "${package_lists}"
  echo Brewfile >> "${package_lists}"
  echo Brewfile.casks >> "${package_lists}"
fi

# Concatenate all package lists
packages="${package_root}/.packages.cat"
cat "${package_lists}" | xargs -I % cat "${package_root}/%" > "${packages}"

# Install using brew bundle.
# Use --no-upgrade to avoid upgrading at this step.
brew bundle --file="${packages}" --no-upgrade

# Clean up temporary file
rm "${packages}"

# Prompt to ask whether to upgrade all Homebrew packages.
brew upgrade -n
read -rp 'Continue? [y/N] ' -n1 ans
if [[ $ans == 'y' ]]; then
  echo
  brew upgrade
fi
