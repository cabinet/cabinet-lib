# Cabinet

This is a password management library that leverages private and public key
cryptography to secure your sensitive data and allowing others to easily
collaborate with you without compromising security.

Note that this is in early stages of development so is not recommended to use
just yet.
For now this is being developed and tested only on Linux.

## Goals / key features

* Secure enough to leave all your data public without worries
* Collaborative without compromising security
* No access given, no data known

* Tag based structure (something like gmail provides)
* distributed (.git)
* Any data that leaves your computer is encrypted

## Vault structure

    $ tree test-vault
    test-vault
    ├── auth
    │   └── key.dat
    ├── data
    │   ├── 9c1e720dd6b044ab9ad711b37d2e3c5d
    │   └── f41c68ca7d864ee8972cbbaae0fbaca2
    └── metadata
        ├── 9133a3a37e1c4eebb6c8c3f924699188
        └── ebefe95d3970495bbd55004edc2e0896


## Files description

Each entry on the vault has 2 files, one for metadata and other for the data.
This separation allows a quick load of all the available information when the
app starts and to keep encrypted the sensitive data (potentially lots of data)
until is needed.

All the files (except on auth) are named randomly so they don't disclose any information.

Here are some examples of how the unencrypted files look.

    on metadata/
    {
        'type': 'account|note|etc',  # templating yeah
        'name': 'the real name for the item',
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

    on auth/people
    {
        'secret': 'here the team secret used to encrypt all the things',
        'admin': 'here the public key?'
        'participants': ['userA', 'userB', 'userC'],  # this defines who is encripted the data for
    }

    on auth/keys.dat
    vault-secret-encrypted-for-user-A
    vault-secret-encrypted-for-user-B
    vault-secret-encrypted-for-user-B
    ...


To be defined:
* participants list has to be signed by admin
* participants list must have the public keys

For the `key.dat` file a user goes through all the lines trying to decipher the
key until hits its own, this prevents anyone from knowing who the participants are.


## Your secret

Your secret key is used to decrypt the vault key, and is stored on
`~/.config/cabinet/secrets/your-name@your-company.com/secret.key`.
