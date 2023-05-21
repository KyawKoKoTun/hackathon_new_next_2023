import hashlib
import secrets


def generate_random_sha256():
    random_string = secrets.token_hex(16)
    sha256_hash = hashlib.sha256(random_string.encode()).hexdigest()
    return sha256_hash


def generate_sha256(string):
    sha256_hash = hashlib.sha256(string.encode()).hexdigest()
    return sha256_hash

