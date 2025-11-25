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

def powmod_inv(a,m):
	def xgcd(a,b):
		if b == 0: return (a,0,1)
		else: 
			gcd,u,v = xgcd(b,a%b)
			return (gcd,v - u*(a//b),u)
	g,_,inv = xgcd(a,m)
	if g !=1:
		ValueError("No inverse")
	return inv%m

# Recover k = nonce
k = (powmod_inv(s1*r2 - s2*r1,n)*(h1*r2 - h2*r1))%n
print(f'{hex(k) = }')

# Recover secret key
x = ((s1*k - h1)*powmod_inv(r1,n))%n 
print(f'{hex(x) = }')

# verify with second secret
s_check = (powmod_inv(k,n)*(h2+x*r2))%n
assert s_check == s2
print(f'Oke nha fen')

def decrypt(priv_key: int, path: str) -> bytes:
	blob = bytearray(open(path,'rb').read())
	print(f'{blob = }')
	key_bytes = priv_key.to_bytes(32,'big')
	print(f'{key_bytes = }')
	keystreams = bytearray()
	counter = 0
	while len(keystreams) < len(blob):
		keystreams.extend(hashlib.sha256(key_bytes + counter.to_bytes(4,'big')).digest())
		counter += 1 
	return bytes(b ^ keystreams[i] for i, b in enumerate(blob))

# decrypt(x,'secret_blob.bin')
print(f'{decrypt(x,'secret_blob.bin') = }')


