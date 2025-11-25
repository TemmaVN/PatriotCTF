#!/usr/bin/env python3
import hashlib
# secp256k1 curve order
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# --- Input signature values ---
r1 = int("288b415d6703ba7a2487681b10da092d991a2ef7d10de016daea4444523dc792", 16)
s1 = int("fc00f6d1c8e93beb4c983104f1991e6d1951aa729004b7a1e841f29d12797f4", 16)
h1 = int("9f9b697baa97445b19c6552e13b3a796ec9b76d6d95190a0c7fab01cce59b7fd", 16)

r2 = int("288b415d6703ba7a2487681b10da092d991a2ef7d10de016daea4444523dc792", 16)
s2 = int("693ee365dd7307a44fddbdd81c0059b5b5f7ef419beee7aaada3c37798e270c5", 16)
h2 = int("465e2cf6b15b701b2d40cac239ab4d50388cd3e0ca54621cff58308f7c9a226b", 16)

def modinv(a, m):
    def egcd(x, y):
        if x == 0:
            return y, 0, 1
        g, s, t = egcd(y % x, x)
        return g, t - (y // x) * s, s

    g, inv, _ = egcd(a % m, m)
    if g != 1:       # inverse does not exist
        ValueError("no inverse")
    return inv % m

# recover nonce: k = (h1 - h2)*(s1 - s2)^(-1) mod n
k = ((h1 - h2) * modinv(s1 - s2, n)) % n
print("Recovered nonce k =", hex(k))

# recover private key: x = r^{-1} (s*k - h) mod n
x = (modinv(r1, n) * (s1 * k - h1)) % n
print("Recovered private key x =", hex(x))

# verify correctness
s_check = (modinv(k, n) * (h1 + r1 * x)) % n
assert s_check == s1, "Verification failed"
print("Private key verified")


def decrypt(priv_key: int, path: str) -> bytes:
    blob = bytearray(open(path, "rb").read())
    key_bytes = priv_key.to_bytes(32, "big")
    keystream = bytearray()
    counter = 0
    while len(keystream) < len(blob):
        keystream.extend(hashlib.sha256(key_bytes + counter.to_bytes(4, "big")).digest())
        counter += 1
    return bytes(b ^ keystream[i] for i, b in enumerate(blob))

print(f'{decrypt(x,'secret_blob.bin') = }')