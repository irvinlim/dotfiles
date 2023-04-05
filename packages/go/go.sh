#!/bin/sh

set -euo pipefail

##
## Helper script to install Go binaries using package list files.
##

if [[ -z "${DOTFILES_ROOT}" ]]; then
    echo "Error: DOTFILES_ROOT not defined"
    exit 1
fi

package_root="${DOTFILES_ROOT}/packages/go"
package_lists="${DOTFILES_ROOT}/.packages-go"

# Skip if go is not installed.
if ! command -v go &> /dev/null
then
    exit
fi

# Generate default package list if not present
if [ ! -f "${package_lists}" ]; then
    touch "${package_lists}"
    echo packages.txt >> "${package_lists}"
fi

# Concatenate all package lists
packages="${package_root}/.packages.cat"
cat "${package_lists}" | xargs -I % cat "${package_root}/%" > "${packages}"

# Install packages from package list
while IFS= read -r pkg; do
    # Skip comments
    comment_regex="^#.*"
    if [[ "${pkg}" =~ $comment_regex ]]; then
        continue
    fi
    
    # Install package
    go install "${pkg}"
done < "${packages}"
