#!/bin/sh

# Skip if go is not installed.
if ! command -v go &> /dev/null
then
    exit
fi

# Install gobin
GO111MODULE=off go get -u github.com/myitcv/gobin

# gobin packages
gobin github.com/rogpeppe/gohack
gobin golang.org/x/tools/cmd/goimports
gobin golang.org/x/tools/cmd/stringer
