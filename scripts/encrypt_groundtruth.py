"""Encrypt groundtruth files to store in the public repository."""

import argparse
import glob
import os
import itertools

from cryptography.fernet import Fernet

import benchmark._crypt

def key_type(arg):
    if os.path.exists(arg) and os.path.isfile(arg):
        with open(arg, "rb") as fh:
            key = fh.read()
        return key
    else:
        arg = str(arg)
        return arg.decode()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt ground truth files")
    parser.add_argument('--pattern', '-p', default = ("benchmark/data/*",), nargs='+')
    parser.add_argument('--key', '-k', default = None, type=key_type)
    parser.add_argument('--store', '-o', default = None)
    args = parser.parse_args()
    if args.key is None:
        args.key = Fernet.generate_key() 
    files = filter(
        lambda v : not v.endswith("secret"),
        itertools.chain.from_iterable(
            glob.glob(pattern)
            for pattern in args.pattern
        )
    )
    for file in files:
        benchmark._crypt.encrypt(file, args.key)
    if args.store is None:
        print(
            f"Encrypted using key: {args.key.decode()}\n"
            f"Make sure to add this key as a github secret (Settings > Secrets > Actions) "
            f"to ensure that the ground truth files can be read during evaluation."
        )
    else:
        with open(args.store, "wb") as fh:
            fh.write(args.key)