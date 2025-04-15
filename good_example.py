# <https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet>
from os import urandom
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password = "input token".encode()  # or some way to get the bytes
# also assuming password is alphanumeric etc, parsing is a whole other issue

salt = urandom(16)  # FIXME need to store the salt somehow
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=3_000_000,
)
key = urlsafe_b64encode(kdf.derive(password))

black_box = Fernet(key)

with open("EXAMPLES.md", "rb") as f:
    plaintext = f.read()

ciphertext = black_box.encrypt(plaintext)
# can write this to a file, re-read it back, whatever
plaintext_new = black_box.decrypt(ciphertext)

print(plaintext_new)
