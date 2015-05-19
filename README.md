# Cabinet

This is a password management library that uses gpg to secure your sensitive
data in a way that you can specify who can access it, this uses gpg
public/private keys.

This project is inspired in http://www.passwordstore.org/

# Access control

    Password store tree
    ├── .gpg-recipients
    ├── Personal
    │   ├── my-gmail-account
    │   └── bank-information
    ├── my-company
    │   ├── .gpg-recipients
    │   ├── business-email-account
    │   └── alarm-code
    ├── some-site
    ├── some-other-site
    └── test-blah

Each folder can have a .gpg-recipients file in its root to specify which users
are going to be able to read the data in there.

If a folder does not have specified a list of people, it will inherit its
parent folder.

The root folder must have a .gpg-recipients file.

The .gpg-recipients file should have a list of name-email-fingerprint to be
descriptive and avoid confusion.

Each time that a user adds a password to that folder, the data is encrypted for
all the people included on the .gpg-recipients file.

Q: how do we prevent some person to add itself to that list?

Maybe file signing for each person allowed to access?
History of changes over signing?

1) persons allowed: me, A, B ... signed by any of the three
2) A added C and signed it
3) C added E and signed it
2) I check signatures back to the point where I signed it and should match.

# Access control 2

    Password store tree
    ├── .auth/
    │   ├── admin
    │   ├── admin-user-A.asc
    │   ├── admin-user-B.asc
    │   └── recipients
    ├── Personal
    │   ├── my-gmail-account
    │   └── bank-information
    ├── my-company
    │   ├── .auth/
    │   │   ├── admin
    │   │   ├── admin-user-A.asc
    │   │   ├── admin-user-C.asc
    │   │   └── recipients
    │   ├── business-email-account
    │   └── alarm-code
    ├── some-site
    ├── some-other-site
    └── test-blah

Each .auth/recipients file has the fingerprints for the users for which the
passwords will be encrypted. If there is no such file the parent's one will be
used. The recipients file will be signed by the group admin.

The admin file contains the fingerprint for the user who is the group admin and
the only one allowed to edit the recipients file.

# File names hiding

We should avoid exposing/hinting which sites we have credentials in.

## Embedded file names

We can use the packets inside the encrypted file name to store/query the
original file name and use some random no significative name as a file name.

The file name is stored by default when you cipher a file with gpg. We can get the original filename as follows:

    gpg -q --list-packets the_encrypted_file.asc 2>&1 | grep --color=never -o 'name=".*"'

The immediate problem is that we can only store the file name itself and not
the whole path. So as a first attempt we could leave the folders as clear text
and just hide the filenames.

Other option could be to store a `.dirname` file in each folder which states
the real name for that folder.


## Random file names

We can use a secret mapping between the actual file names and some random
generated ones.  An idea for this is matter: `random_tree.py`

The password store may look like this:

    Password store tree
    ├── .gpg-recipients
    ├── F6zYkOJVLYXTCsDV4KUfm5H5NcMisX3eS5F20OTTgrU=
    │   ├── Prcicxh4HUWIXWjJRHNfmRi_5WL0k71SZkg-FMZq_YU=
    │   ├── QlqbNnmUBM3b1EzHlPHCs8rFDNBiBbrYZ7R88JcwYbE=
    │   └── xxBZatC6zx_MreJffgFhIbfAurVkBzreaiW_S-yWLD8=
    ├── S6mLxBWIYLKGPfQI4XHsz5U5ApZvfK3rF5S20BGGteH=
    │   ├── .gpg-recipients
    │   ├── Cepvpku4UHJVKJwWEUAszEv_5JY0x71FMxt-SZMd_LH=
    │   └── kkOMngP6mk_ZerWsstSuVosNheIxOmernvJ_F-lJYQ8=
    ├── FdhdC2fXEwB_sh4lM7VenQSWKtb6o1Wjpkjh27KESiU=
    ├── PffBZcz-K0QR8ENyT8RC5JuCoyKdNeh0W5UIy0nzbrE=
    └── sgEG-FOqFs2EzTCJxG-6a5AaWGQ-ROXqR0-VmSz-2wk=


Q: how do we store the mapping in a way that the right people can access it?

Maybe we can use a specific file to map 'real name' -> 'random name' along with
each `.gpg-recipients` file, encrypted with all the people listed on
`.gpg-recipients`.


# Project name

Possible project name

* Cabinet
http://www.ironmongeryforyou.co.uk/images/P/AB-KS300_300_adjustable_hook_key_cabinet-01.jpg
