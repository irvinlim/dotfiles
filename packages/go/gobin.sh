#!/bin/sh

# Skip if go is not installed.
if ! command -v go &> /dev/null
then
    exit
fi

# Install gobin
GO111MODULE=off go get -u github.com/myitcv/gobin

# gobin packages
go install github.com/rogpeppe/gohack@latest
go install golang.org/x/tools/cmd/goimports@latest
go install golang.org/x/tools/cmd/stringer@latest
