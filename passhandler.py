import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def hash(dbpassword,data,salt):
    #salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(dbpassword)) # Can only use kdf once
    f=Fernet(key)
    encrypted = f.encrypt(data)
    return encrypted

def dehash(dbpassword,encrypted,salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(dbpassword))
    f=Fernet(key)
    while True:
        try:
            decrypted = f.decrypt(encrypted)
            decrypted_decoded = decrypted.decode()
            return decrypted_decoded
        except:
            incorrect_password = "Different password used to encrypt data"
            return incorrect_password
