from passlib.hash import argon2

def hash_password(password: str):
    return argon2.hash(password)

def verify_password(password: str, hash):
    return argon2.verify(password, hash)

def create_user(email, password):
    pass