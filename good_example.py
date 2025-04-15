# <https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet>
from os import urandom, path
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password = "input token".encode()  # or some way to get the bytes
# also assuming password is alphanumeric etc, parsing is a whole other issue

# store salt file next to log file
log_file = "EXAMPLES.md"  # or whatever we get from input
salt_file = path.dirname(log_file)
if salt_file == "":
    salt_file = "."
salt_file += "/salt"

# if it's already stored, read it; otherwise make new salt
if path.exists(salt_file):
    with open(salt_file, "rb") as f:
        salt = f.read()
else:
    salt = urandom(16)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=3_000_000,
)
key = urlsafe_b64encode(kdf.derive(password))

black_box = Fernet(key)

with open(log_file, "rb") as f:
    plaintext = f.read()

ciphertext = black_box.encrypt(plaintext)
# can write this to a file, re-read it back, whatever
plaintext_new = black_box.decrypt(ciphertext)

print(plaintext_new)

# save salt to file for later
with open(salt_file, "wb") as f:
    f.write(salt)
