from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


def create_hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hash: str) -> bool:
    try:
        ph.verify(hash, password)
    except VerifyMismatchError:
        return False
    return True
