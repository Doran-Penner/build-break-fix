# <https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet>
from os import urandom, path
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pickle
from typing import Optional


class Event:
    def __init__(self, time, employee, name, arrive, room):
        # time the event happened
        self.time: int = time
        # if it's an employee (True) or a guest (False)
        self.employee: bool = employee
        # the person's name
        self.name: str = name
        # if they're arriving (True) or leaving (False)
        self.arrive: bool = arrive
        # the room, if None then they're entering/leaving the whole gallery
        self.room: Optional[int] = room

    # nicely-formatted printing
    def __str__(self):
        return (
            f"At time {self.time} "
            f"{'employee' if self.employee else 'guest'} "
            f"{self.name} "
            f"{'arrived in' if self.arrive else 'left'} "
            f"{f'room {self.room}' if self.room is not None else 'the gallery'}"
        )

    __repr__ = __str__


# get these from arg parsing
password = "input token".encode()
log_file = "./logfile"

# decide salt file location and load or generate it
salt_file = path.dirname(log_file)
if salt_file == "":
    salt_file = "."
salt_file += "/salt"

if path.exists(salt_file):
    with open(salt_file, "rb") as f:
        # NOTE: we explicitly do not use pickle on the salt file,
        # that would be insecure and we don't need it
        salt = f.read()
else:
    salt = urandom(16)


# make key for encryption
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=3_000_000,
)
key = urlsafe_b64encode(kdf.derive(password))
black_box = Fernet(key)


# load log if it already exists
if path.exists(log_file):
    with open(log_file, "rb") as f:
        ciphertext = f.read()
    plaintext = black_box.decrypt(ciphertext)
    log: list[Event] = pickle.loads(plaintext)
else:
    # initialize empty log
    log: list[Event] = []

##### NOW WE CAN DO STUFF WAHOO

log.append(Event(2, True, "Jane", True, 1))

print(log)  # for debugging, remove before submission TODO

##### THE END OF DOING STUFF


# save salt and log for next call
with open(salt_file, "wb") as f:
    f.write(salt)
with open(log_file, "wb") as f:
    enc_log = black_box.encrypt(pickle.dumps(log))
    f.write(enc_log)
