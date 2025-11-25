#!/usr/bin/env python3

from hashlib import md5
from tqdm import tqdm
enc = '3a52fc83037bd2cb81c5a04e49c048a2'
with open('/usr/share/wordlists/rockyou.txt','rb') as f:
	for data in tqdm(f):
		if len(data) < 2: continue
		if not ord('0') <= data[-1] <= ord('9') and ord('0') <= data[-2] <= ord('0'): continue
		check = md5(data.rstrip()).hexdigest()
		if check == enc: 
			print(f'{check = }')
			break