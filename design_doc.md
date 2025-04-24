# Build it
Heath Nevis, Ryan Koeninger, Doran Penner\
2025 April 24

All code can be found [on the GitHub repository](https://github.com/Doran-Penner/build-break-fix), which includes technical documentation and source code; this document is a high-level overview of our design and security considerations.

## Overall method

While `logappend`/`logread` is running, we keep all the log data in memory and only read/write and the beginning/end of the program. The log itself is just a Python list of structs that contain the event's info, such as when it happened, the relevant room, and so on. To append, we create a new `Event` with all the needed data; to query, we do many loops and filters through this list. For saving, we first encrypt the serialized data using `ChaCha20-Poly1305`, a standard algorithm in OpenSSL which additionally signs the encrypted data, and a password derived from the token. Then we write the encrypted data along with nonce & password salt to a single output file. This ensures security, since we will never attempt to deserialize data unless it successfully authenticates & decrypts; and if the salt or nonce is modified, the authentication will also fail.

## Security concerns & defenses

### Injection / untrusted data

There are many angles to use malicious data:

1. the (encrypted) log bytes themselves in the file can be maliciously-crafted to get the program to attempt decryption of untrusted data;
2. the salt/nonce can be modified directly, possibly allowing for similar attacks;
3. and the command line takes arbitrary strings.

To solve 1, we only attempt decryption if the signature matches (default behavior in `ChaCha20-Poly1305`). For the second there isn't much to do, but the decryption should only work if those are the correct values, and it's cryptographyically safe to reveal the salt and nonce in any case. As for command-line injection, we use a standard argument-parsing library which (to our knowledge) does not have injection vulnerabilities.

### Unsafe cryptography

The simplest encryption scheme we could find was Fernet from the `cryptography` library. But it turns out this has a known vulnerability! With a [padding oracle attack](https://robertheaton.com/2013/07/29/padding-oracle-attack/) we could leak almost everything in the log (though it's annoying to implement). To solve this, we changed to a different encryption schema using the `ChaCha20` block cipher with the `Poly1305` authenticator, defined [here](https://datatracker.ietf.org/doc/html/rfc7539.html).

### Log length

With only a couple of logged events, an attacker can learn some information about the state of the museum --- for example, an upper bound on the number of guests. To combat this, we add a random number of `None` values to the serialized log before writing to disk (about 400 on average) and remove those when reading into memory. This still leaks a very small amount of information, but it's a **very** small confidence increase for an attacker.

### Mid-process interruption

If an attacker cancels our porgram mid-run, what can they learn? Besides memory inspection (outside the scope of what we can defend against), they shouldn't be able to learn anything new from the written logfile or sneak in untrusted data. To combat this, we only read or write to/from disk once each; at the start to get all of the saved data, and at the end to save a new log (if `logappend`ing). This way an attacker cannot, say change our password salt mid-operation.

***

Beyond those specific concerns, we followed generally good principles --- never re-use a nonce, don't rely on hidden source code, and so on.
