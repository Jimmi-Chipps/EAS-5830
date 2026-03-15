#!/usr/bin/env python3
import random
from eth_account.messages import encode_defunct
from web3 import Web3
import sys


def validate(code_path):
    try:
        import signatures
    except Exception as e:
        print( f"Could not load signatures.py\n{e}" )
        sys.exit(1)

    required_methods = ["sign", "verify"]
    for m in required_methods:
        if m not in dir(signatures):
            print( f"{m} not defined" )
            sys.exit(1)

    num_tests = 5
    num_passed = 0
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    PKs = []
    w3 = Web3()
    for ct in range(num_tests):
        m = "".join([random.SystemRandom().choice(characters) for _ in range(32)])
        try:
            pk, sig = signatures.sign(m)
        except Exception as e:
            print(f"sign failed to complete:\n{e}")
            continue
        message = encode_defunct(text=m)
        valid = pk == w3.eth.account.recover_message(message, signature=sig.signature)

        if not valid:
            print("The signature returned did not verify")
            continue

        good_message = True
        if random.randint(0, 1) == 1:
            m = "".join([random.SystemRandom().choice(characters) for _ in range(32)])
            good_message = False
        verified = good_message == signatures.verify(m, pk, sig)

        new_pk = True
        for i in range(len(PKs)):  # pk is an unhashable type
            if pk == PKs[i]:
                new_pk = False
        if new_pk:
            print(f"\t[\033[92mSUCCESS\033[00m]\tPublic key is unique for test #{ct}")
            num_passed = num_passed + 1
            PKs.append(pk)
        else:
            print(f"\t[\033[91mFAILED\033[00m]\tPublic key is not unique for test #{ct}")

        if valid:
            print(f"\t[\033[92mSUCCESS\033[00m]\tYour message signature is correct for test #{ct}")
            num_passed = num_passed + 1
        else:
            print(f"\t[\033[91mFAILED\033[00m]\tYour message signature is incorrect for test #{ct}")

        if verified:
            print(f"\t[\033[92mSUCCESS\033[00m]\tYou correctly verified the signature for test #{ct}\n")
            num_passed = num_passed + 1
        else:
            print(f"\t[\033[91mFAILED\033[00m]\tYou incorrectly verified the signature for test #{ct}\n")

    return 100 * num_passed / (3 * num_tests)

if __name__ == "__main__":
    print( validate("") )
