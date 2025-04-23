import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pickle
import typing


"""
HOW TO USE

```py
import loadsave
log = loadsave.load_all(password, log_file)
# ... whatever you wanna do in here
save_all(log, password, log_file)
```

And then you're done! You shouldn't need to use
anything else in loadsave, just those two functions.
"""


class Event:
    def __init__(
        self,
        time: int,
        employee: bool,
        name: str,
        arrive: bool,
        room: typing.Optional[int],
    ):
        # time the event happened
        self.time = time
        # if it's an employee (True) or a guest (False)
        self.employee = employee
        # the person's name
        self.name = name
        # if they're arriving (True) or leaving (False)
        self.arrive = arrive
        # the room, if None then they're entering/leaving the whole gallery
        self.room = room

    # nicely-formatted printing (note: NOT to spec, for debuggging)
    def __str__(self):
        return (
            f"At time {self.time} "
            f"{'employee' if self.employee else 'guest'} "
            f"{self.name} "
            f"{'arrived in' if self.arrive else 'left'} "
            f"{f'room {self.room}' if self.room is not None else 'the gallery'}"
        )

    __repr__ = __str__


def get_adj_path(name: str, log_file: str) -> str:
    adj_file = os.path.dirname(log_file)
    if adj_file == "":
        adj_file = "."
    adj_file += "/" + name
    return adj_file


def get_salt(log_file: str) -> bytes:
    salt_file = get_adj_path("salt", log_file)
    if os.path.exists(salt_file):
        with open(salt_file, "rb") as f:
            # NOTE: we explicitly do not use pickle on the salt file,
            # that would be insecure and we don't need it
            salt = f.read()
    else:
        salt = os.urandom(16)
    return salt


def get_nonce(log_file: str, decrypting: bool) -> bytes:
    file_path = get_adj_path("nonce", log_file)
    if os.path.exists(file_path) and decrypting:
        with open(file_path, "rb") as f:
            nonce = f.read()
    else:
        nonce = os.urandom(12)
    return nonce


def save_adj(name: str, val: bytes, log_file: str):
    file_path = get_adj_path(name, log_file)
    with open(file_path, "wb") as f:
        f.write(val)


# <https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet>
def get_black_box(password: str, salt: bytes) -> ChaCha20Poly1305:
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=1_000_000,
    )
    key = kdf.derive(password.encode())
    return ChaCha20Poly1305(key)


def load_all(password: str, log_file: str) -> list[Event]:
    if os.path.exists(log_file):
        salt = get_salt(log_file)
        nonce = get_nonce(log_file, True)
        black_box = get_black_box(password, salt)
        with open(log_file, "rb") as f:
            ciphertext = f.read()
        return pickle.loads(black_box.decrypt(nonce, ciphertext, None))
    else:
        return []


def save_all(log: list[Event], password: str, log_file: str):
    salt = get_salt(log_file)
    nonce = get_nonce(log_file, False)
    black_box = get_black_box(password, salt)
    # ideally we save the nonce and salt as added & auth'd data via chachapoly
    # but I can't figure out how to read that so we'll do the normal thing
    enc_log = black_box.encrypt(nonce, pickle.dumps(log), None)
    with open(log_file, "wb") as f:
        f.write(enc_log)
    save_adj("salt", salt, log_file)
    save_adj("nonce", nonce, log_file)


# log: list[Event] = load_all("sekwet pasword :3", "./logfile")
# log.append(Event(2, True, "Jane", True, 1))
# print(log)
# save_all(log, "sekwet pasword :3", "./logfile")
