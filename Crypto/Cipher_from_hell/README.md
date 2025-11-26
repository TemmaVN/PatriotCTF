# Cipher from hell
## Challange 
- Source code tạo mã: [encryptor.py](https://github.com/TemmaVN/PatriotCTF/blob/master/Crypto/Cipher_from_hell/encryptor.py)
- Cipher bytes: [encrypted](https://github.com/TemmaVN/PatriotCTF/blob/master/Crypto/Cipher_from_hell/encrypted)
## Solving
- Mục đích chính của đoạn mã là phân tích plaintext thành:
```pl = a1*3**c + a2*3**(c-1) + a3*3**(c-2) + ....```
- Dựa vào ```a1,a2...``` và để ý đoạn```ss += o[s//3**c][s%3]```
- Ta có thể suy ra được dựa trên ss để suy ngược lại ```ai```
```
o = (
	(6, 0, 7),
	(8, 2, 1),
	(5, 4, 3)
)
while c > -1:
	ss *= 9
	ss += o[s//3**c][s%3]
	s -= s//3**c*3**c
	s //= 3
	c -= 2
print(ss.to_bytes(math.ceil(math.log(ss, 256)), byteorder='big'))
```
- Nhìn lại hàm tạo mã, ta thấy dạng mã ```enc = o[an,a1]*9**(c//2) .....``` và ta suy ra được `[ai]` bằng các bước giải ngược lại.
- Step 1: Phân tích enc thành dạng ```[b1,b2...bn]``` thỏa ```enc = b1*9**(c//2)...``` 
- Step 2: Trích ```bi``` trên mảng o và truy ngược```a1,a2,...an```.
- Step 3: Chuyển `Plaintext` thành byte và ta được flag!!
- Code python (hơi xấu): [solve.py](https://github.com/TemmaVN/PatriotCTF/blob/master/Crypto/Cipher_from_hell/solve.py)
- FLag là: `pctf{a_l3ss_cr4zy_tr1tw1s3_op3r4ti0n_f37d4b}`