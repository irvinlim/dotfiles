#!/bin/sh

# Install gobin
GO111MODULE=off go get -u github.com/myitcv/gobin

# gobin packages
gobin github.com/rogpeppe/gohack
gobin golang.org/x/tools/cmd/goimports
gobin golang.org/x/tools/cmd/stringer
