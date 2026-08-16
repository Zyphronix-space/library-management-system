import hashlib
import os
import binascii

# PBKDF2-HMAC-SHA256 with a random per-password salt. Stdlib-only (no bcrypt
# dependency), but salted + stretched so it's not reversible plaintext like
# the passwords used to be stored as.
_ITERATIONS = 100_000


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, _ITERATIONS)
    return binascii.hexlify(salt).decode() + ':' + binascii.hexlify(derived).decode()


def verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, hash_hex = stored.split(':')
        salt = binascii.unhexlify(salt_hex)
        derived = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, _ITERATIONS)
        return binascii.hexlify(derived).decode() == hash_hex
    except (ValueError, binascii.Error):
        return False
