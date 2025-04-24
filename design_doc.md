# Build it
Heath Nevis, Ryan Koeninger, Doran Penner\
2025 April 24

All code can be found [on the GitHub repository](https://github.com/Doran-Penner/build-break-fix), which includes technical documentation and source code; this document is a high-level overview of our design and security considerations.

## Overall method

While `logappend`/`logread` is running, we keep all the log data in memory and only read/write and the beginning/end of the program. The log itself is just a Python list of structs that contain the event's info, such as when it happened, the relevant room, and so on. To append, we create a new `Event` with all the needed data; to query, we do many loops and filters through this list. For saving, we first encrypt the serialized data using `ChaCha20-Poly1305`, a standard algorithm in OpenSSL which additionally signs the encrypted data, and a password derived from the token. Then we write the encrypted data along with nonce & password salt to a single output file. This ensures security, since we will never attempt to deserialize data unless it successfully authenticates & decrypts; and if the salt or nonce is modified, the authentication will also fail.

## Security concerns & defenses

TODO:

- untrusted data / injection (salt/nonce is fine, only unpickle verified data, use parsing library for safety)
- bad crypto (use better method)
- log length (gaussian noise)
- mid-process interruption (only read/write in one go)
