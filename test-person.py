#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from cabinet.person import Person


def main():
    test_path = os.path.join(os.getcwd(), 'test-persons-data')

    alice = Person('alice', test_path)
    alice.generate_keys()
    bob = Person('bob', test_path)
    bob.generate_keys()

    message = b"Hello bob, how are you doing?"
    encrypted = alice.encrypt(message, bob.public_key)
    decrypted = bob.decrypt(encrypted, alice.public_key)
    # decrypted = alice.decrypt(encrypted, alice.public_key)  # error!
    import base64
    b64enc = base64.b64encode(encrypted)

    print("=== People ===")
    print("Alice public key:", str(alice.get_public_key()))
    print("Alice public key length:", len(str(alice.get_public_key())))
    print("Bob public key:", str(bob.get_public_key()))

    print("Bob *private* key :", bob._get_private_key(True))
    bpk1 = bob._get_private_key()
    pw = b'test'
    bob.save_key(pw)
    bob.load_key(pw)
    bpk2 = bob._get_private_key()
    print("Bob *private* key :", bob._get_private_key(True))
    print(bpk1 == bpk2)

    print()
    print("=== Clear Text ===")
    print("Message:", message)
    print("Message length:", len(message))

    print()
    print("=== Encrypted ===")
    print("Message:", encrypted)
    print("Message length:", len(encrypted))
    print("Message, base 64:", b64enc)
    print("Message length, base 64:", len(b64enc))

    print()
    print("=== Decrypted ===")
    print("Message:", decrypted)

if __name__ == "__main__":
    main()
