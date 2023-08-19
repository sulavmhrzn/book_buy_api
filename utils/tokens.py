from uuid import uuid4


def generate_token() -> str:
    return uuid4().hex
