import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pickle
import typing
import math
import random


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

The format of the saved logfile is ciphertext || salt || nonce,
where salt is set once when the log is created and the
nonce is re-randomized every time we modify the file.
"""

SALT_LENGTH = 16
NONCE_LENGTH = 12


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


def load_all(password: str, log_file: str) -> tuple[list[Event], bytes]:
    if os.path.exists(log_file):
        with open(log_file, "rb") as f:
            ciphertext = f.read()
        salt = ciphertext[-(SALT_LENGTH + NONCE_LENGTH) : -(NONCE_LENGTH)]
        nonce = ciphertext[-(NONCE_LENGTH):]
        ciphertext = ciphertext[: -(SALT_LENGTH + NONCE_LENGTH)]
        black_box = get_black_box(password, salt)
        log = pickle.loads(black_box.decrypt(nonce, ciphertext, None))
        # remove random Nones
        log = [event for event in log if event is not None]
    else:
        log = []
        salt = os.urandom(SALT_LENGTH)
    # If we don't keep salt in memory, attacker can overwrite salt between
    # load & save and then they get to decide our salt. Not sure what the
    # exact attack is there, but it feels like a bad idea!
    return log, salt


def save_all(log: list[Event], salt: bytes, password: str, log_file: str):
    # add a bunch of Nones to hide length:
    # they still technically get some info but it's not much
    log.extend(None for _ in range(max(math.floor(random.gauss(400, 100)), 0)))
    nonce = os.urandom(12)
    black_box = get_black_box(password, salt)
    enc_log = black_box.encrypt(nonce, pickle.dumps(log), None)
    enc_log += salt + nonce
    with open(log_file, "wb") as f:
        f.write(enc_log)


# log: list[Event]
# log, salt = load_all("sekwet pasword :3", "./logfile")
# log.append(Event(2, True, "Jane", True, 1))
# print(log)
# save_all(log, salt, "sekwet pasword :3", "./logfile")
