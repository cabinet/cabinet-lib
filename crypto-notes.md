PyNaCl currently only exposes Box, which uses a private-public key derivation.
The sealed box is not exposed yet so we need to know who encrypted the message beforehand.

I'll test cryptography then...

encrypt key, add public key... done... pynacl it is


# Team: git repo, set of public keys

Team/
.git/  <- git standard dir

.config/
    // users-public-keys.json
    known-remotes.json

group/
    .auth/
        users-public-keys.json
        group-key.json
        keys.json
    fileA
    fileB
    fileC


* group/.auth/users-public-keys.json
There's a need for an unique identifier across teams (git repos) - email?
Each public key needs to be signed by the admin.
content:
{
    "emailA": ["public key A", "admin's verification signature"],
    "emailB": ["public key B", "admin's verification signature"],
    ...
}

* group/.auth/group-key.json
No key is added to emailN if it's key isn't signed by the admin.
content:
{
    "emailA": "key encrypted for emailA",
    "emailB": "key encrypted for emailB",
    ...
}


Problem!
The recipients file may be signed by the admin, but that file can be moved to a
different group and won't be noticed.
- group nonce to solve this?... the group's encrypted key with admin's public key.
how the users can tell if the recipients file is the right one?
- group name on top + admin's signature?

Problem
users not in a group shouldn't know about users in the group

Problem:
if a user gets added and then removed to a group, that user could revert the
commit and be part of that group again... we need to make sure that git commits
changes to a file are done by the admin and the commit is signed by admin.
We also don't want that people outside the group know about people involved by
commit history so we should encrypt the commit data as well (with group key)


One user
========

first use case, to get something working.

Config dir, check for private key, encrypted, ask for password.
Encrypted key/value store... with files

Ideas
=====

Tag based structure

why git:
- minimize conflicts on team updates
- well proven file sharing, history tracking

Local encrypted cache for faster load


Key features
============

* Tag based structure (gmail like)
* distributed (.git)
* Zero Knowledge

File structure
==============

store/
    data/
    metadata/
    auth/


Each entry has 2 files for metadata and data respectively.
On app start all the metadata is read (and kept in memory) to build the "tree"
or list of available passwords, the encrypted file will be loaded only on
demand.

on metadata/
{
    'type': 'account|note|etc',  # templating yeah
    'filename': 'the-real-file-name.ext',  # TODO: filename or name?
    'hashname': 'random hash as actual filename on filesystem'
    'tags': ['personal', 'secret', 'blah'],
    'version': 'the version of the app that created/changed this file the last time (for compatibility)'
}

on data/
{
    'username': 'my-cool-username-on-site-X',
    'password': 'supersecretpassword',
    'site url': 'https://example.com',
    'notes': 'some notes if you want to',

    'custom field': '*maybe* allow for custom fields'
}

on auth/
{
    'secret': 'here the team secret used to encrypt all the things',
    'admin': 'here the public key?'
    'participants': ['userA', 'userB', 'userC'],  # this defines who is encripted the data for
    ^ maybe public keys here?
}

maybe participants list has to be signed by admin

keys.dat
secret-encrypted-for-user-A
secret-encrypted-for-user-B
secret-encrypted-for-user-B
...

(each user goes through all the lines trying to decipher the key until hits its own)


App
===

0) load my secret key from config path
1) get secret key, from known file, the one encrypted for me.
2) go through all metadata/ files, decrypt and load them to build the data on memory.
3) ask for file 'X': search on metadata, find the hashname, decrypt it and bring its contents.
4) save file 'X': add metadata (encrypted to disk and plain in memory) and file contents encrypted on disk.

load metadata file:
- needs filename
- read filename
- decrypt it
- parse json
- return object

Initialization - first use, keys creation:
- create key pair and save it in config directory

Initialization - vault creation:
- generate Vault secret key
- add admin public key to auth data
- add admin as participant on auth data

Vault object?
with key and helpers to add and remove items, parameter encryptor/decryptor to handle crypto


Two layers needed: auth layer + vault

* auth: users list (for vault key encryption) and signatures of users added by the admin, plus my signature on admin's public key.
a normal user almost won't use the auth layer, just to retrieve the vault key encrypted for itself
the vault admin will though, to verify the list of users, add new users, rotate keys, etc...

* vault: store/retrieve data, one key
