#!/usr/bin/env python3

nums = open('keystream_leak.txt','r').read().splitlines()
nums = list(map(int,nums))
print(f'{nums = }')

cipher_text = list(open('cipher.txt','rb').read())
print(f'{cipher_text = }')

out = [(num & 0xFF)^b for num, b in zip(nums,cipher_text)]
print(f'{bytes(out) = }')