#!/bin/sh

exit  # remove this to test, be careful on not to cipher/overwrite your files
cd gpg.test/test-files-tree  # files and directories to encrypt/decrypt as a test
for f in $(find . -type f); do gpg --no-use-agent -c --batch --yes --passphrase-file `pwd`/../key -o $f $f; done;  # encrypt files
for f in $(find . -type f); do gpg -q --list-packets --no-use-agent --passphrase-file `pwd`/../key $f 2>&1 | grep --color=never -o 'name=".*"'; done;  # list files names
