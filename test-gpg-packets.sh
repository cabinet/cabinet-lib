#!/bin/bash

[[ -z $1 ]] && exit

KEY=`pwd`/test_passphrase_file.txt
cd gpg.test/test-files-tree  # files and directories to encrypt/decrypt as a test

if [[ $1 == "encrypt" ]]; then
    for f in $(find . -type f); do
        gpg --no-use-agent -c --batch --yes --passphrase-file $KEY -o $f $f;
    done
fi

if [[ $1 == "list" ]]; then
    for f in $(find . -type f); do
        gpg -q --list-packets --no-use-agent --passphrase-file $KEY $f 2>&1 | grep --color=never -o 'name=".*"';
    done;
fi
