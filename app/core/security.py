"""Security helpers prepared for future JWT authentication."""


def get_password_hash(password: str) -> str:
    raise NotImplementedError("Password hashing will be implemented with the auth module.")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    raise NotImplementedError("Password verification will be implemented with the auth module.")

