#!/usr/bin/env python3

import math
from Crypto.Util.number import long_to_bytes as l2b
with open('encrypted','rb') as f:
	enc = f.read().rstrip()

enc_int = int.from_bytes(enc)
print(f'{enc_int = }')

o = (
	(6, 0, 7),
	(8, 2, 1),
	(5, 4, 3)
)

def find_in_o(num):
	for i,row in enumerate(o):
		for j,value in enumerate(row):
			if num == value: return i,j
	return None
c = math.floor(math.log(enc_int,9))
enc_arr = []
while c > -1:
	enc_arr.append(enc_int//9**c)
	enc_int -= enc_int//9**c*9**c 
	c -= 1 
print(f'{find_in_o(8)[1] = }')
print(F'{o[1][0] = }')
left_arr = []
right_arr = []
for tst in enc_arr:
	left, right = find_in_o(tst)
	left_arr.append(left)
	right_arr.append(right)
print(f'{left_arr = }')
print(f'{right_arr = }')
fin_arr = (right_arr + left_arr[::-1])
print(f'{fin_arr = }')
res = 0
for i,num in enumerate(fin_arr):
	res += num*3**i
print(f'{l2b(res) = }')
