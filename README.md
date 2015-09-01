# Cabinet

This is a password management library that uses gpg to secure your sensitive
data in a way that you can specify who can access it, this uses gpg
public/private keys.

This project was inspired in http://www.passwordstore.org/

Note that this is in early stages of development so is not recommended to use
just yet.


# Vault structure

    Vault root                       Vault root on disk
    ├── .auth/                       ├── .auth/
    │   ├── admin                    │   ├── admin
    │   ├── admin-user-A.asc         │   ├── admin-user-A.asc
    │   ├── admin-user-B.asc         │   ├── admin-user-B.asc
    │   └── recipients               │   └── recipients
    ├── Personal                     ├── F6zYkOJVLYXTCsDV4KUfm5H5NcMisX3eS5F20OTTgrU
    │   ├── my-gmail-account         │   Prcicxh4HUWIXWjJRHNfmRi_5WL0k71SZkg
    │   └── bank-information         │   QlqbNnmUBM3b1EzHlPHCs8rFDNBiBbrYZ7R88JcwYbE
    ├── my-company                   ├── xxBZatC6zx_MreJffgFhIbfAurVkBzreaiW_S
    │   ├── .auth/                   │   ├── .auth/
    │   │   ├── admin                │   │   ├── admin
    │   │   ├── admin-user-A.asc     │   │   ├── admin-user-A.asc
    │   │   ├── admin-user-C.asc     │   │   ├── admin-user-C.asc
    │   │   └── recipients           │   │   └── recipients
    │   ├── business-email-account   │   ├──  S6mLxBWIYLKGPfQI4XHsz5U5ApZvfK3rF5S20BGGteH
    │   └── alarm-code               │   └──  Cepvpku4UHJVKJwWEUAszEv_5JY0x71FMxt
    ├── some-site                    ├── kkOMngP5mk_ZerWsstSuVosNheIxOmernvJ_F
    ├── some-other-site              ├── FdhdC2fXEwB_sh4lM7VenQSWKtb6o1Wjpkjh27KESiU
    └── test-blah                    └── PffBZcz-K0QR8ENyT8RC5JuCoyKdNeh0W5UIy0nzbrE

## Access control

Each `.auth/recipients` file has the fingerprints for the users for which the
passwords will be encrypted. If there is no such file the parent's one will be
used. The recipients file will be signed by the group admin.

The `admin` file contains the fingerprint for the user who is the group admin
and the only one allowed to edit the recipients file.

Each user in `.auth/recipients` signs the `.auth/admin` file right after
verifying the fingerprint on it. Thus, user 'user-A' will generate a file
called `.auth/admin-user-A.asc`.

In order to be considered valid, each data file has to be signed by either the
group admin or a user in the recipients file.


## File names hiding

To avoid exposing/hinting which sites we have credentials in we use a secret
mapping between each real file name and a random generated one.

To store the mappings in a way that the right people can access it we use a
specific file to map 'real name' -> 'random name' on each `.auth/` folder. This
file is encrypted for each person in the `recipients` file


## Storage

The vault is stored on `~/.config/cabinet/vault/`, this folder will be stored on
a git repo and a wrapper will be created to automate git workflow. Combining
git with file-level password storage allows a group of people to work over a
vault of passwords without facing edit/sync conflicts.


# Keys

Cabinet will use a separate set of keys for encrypting, not the system's gnupg ones.

Keys are stored on `~/.config/cabinet/gnupg/`.
