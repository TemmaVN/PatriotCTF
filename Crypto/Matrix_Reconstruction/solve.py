#!/usr/bin/env python3

import numpy as np

# Dữ liệu
ciphertext_hex = "6caa d8c8 a408 48f2 0000 9de6 c734 4c7b 9c03 f5be bca9 6219 3aef 4a84 ad39 7a99 ff04 f4"
ciphertext = bytes.fromhex(ciphertext_hex.replace(" ", ""))

leaked_states = [
    2694419740, 2430555337, 3055882924, 228605358, 4055459295,
    676741477, 1030306057, 1320993926, 2317712498, 3680836913,
    1922319333, 1836782265, 1490734773, 218490631, 4065897775,
    3125259028, 189241330, 1710684784, 2355890305, 95797196,
    813001417, 1021781706, 3522243094, 1603928614, 1122416469,
    4125638785, 2423341845, 3666529189, 61609182, 2391267942,
    148130332, 4246509548, 3552866507, 1487751530, 1895017353,
    3277260507, 4251037246, 22647618, 3958787364, 227107204
]

def to_bits(n, length=32):
    """Chuyển số sang vector bit (LSB first)"""
    return [(n >> i) & 1 for i in range(length)]

def from_bits(bits):
    """Chuyển vector bit sang số"""
    return sum(b << i for i, b in enumerate(bits))

def gf2_matrix_multiply(A, v):
    """Nhân ma trận A với vector v trên GF(2)"""
    result = []
    for row in A:
        result.append(sum(a * b for a, b in zip(row, v)) % 2)
    return result

def gf2_solve(equations, results):
    """Giải hệ phương trình tuyến tính trên GF(2) bằng Gaussian elimination"""
    n = len(equations)
    m = len(equations[0])
    
    # Tạo ma trận mở rộng
    aug = [equations[i] + [results[i]] for i in range(n)]
    
    # Gaussian elimination
    pivot_row = 0
    for col in range(m):
        # Tìm pivot
        found = False
        for row in range(pivot_row, n):
            if aug[row][col] == 1:
                # Swap rows
                aug[pivot_row], aug[row] = aug[row], aug[pivot_row]
                found = True
                break
        
        if not found:
            continue
        
        # Eliminate
        for row in range(n):
            if row != pivot_row and aug[row][col] == 1:
                for c in range(m + 1):
                    aug[row][c] ^= aug[pivot_row][c]
        
        pivot_row += 1
    
    # Back substitution
    solution = [0] * m
    for row in range(min(pivot_row, m)):
        # Tìm leading 1
        for col in range(m):
            if aug[row][col] == 1:
                solution[col] = aug[row][m]
                break
    
    return solution

print("=== Bước 1: Khôi phục ma trận A ===")
print(f"Số states bị leak: {len(leaked_states)}")

# Chuyển states sang dạng bit
states_bits = [to_bits(s) for s in leaked_states]

# Xây dựng hệ phương trình để tìm A
# S[n+1] XOR B = A * S[n]
# Với 3 states liên tiếp: S0, S1, S2
# S1 XOR B = A * S0
# S2 XOR B = A * S1
# => S2 XOR S1 = A * S1 XOR A * S0 = A * (S1 XOR S0)

print("\nTạo hệ phương trình từ các state liên tiếp...")
A = [[0] * 32 for _ in range(32)]

# Sử dụng phương pháp loại bỏ B: S[i+1] XOR S[i+2] = A*S[i] XOR A*S[i+1]
equations = []
results = []

for i in range(len(leaked_states) - 2):
    s0 = states_bits[i]
    s1 = states_bits[i + 1]
    s2 = states_bits[i + 2]
    
    # s1 XOR s2 = A*(s0 XOR s1)
    lhs = [s0[j] ^ s1[j] for j in range(32)]
    rhs = [s1[j] ^ s2[j] for j in range(32)]
    
    equations.append(lhs)
    results.append(rhs)

print(f"Số phương trình: {len(equations)}")

# Giải cho từng bit của mỗi hàng của A
print("Giải hệ phương trình GF(2)...")
A_recovered = []
for bit_pos in range(32):
    # Lấy bit thứ bit_pos từ mỗi result
    rhs_for_bit = [r[bit_pos] for r in results]
    
    # Giải hệ phương trình
    row = gf2_solve(equations, rhs_for_bit)
    A_recovered.append(row)

print("✓ Đã khôi phục ma trận A")

print("\n=== Bước 2: Tìm vector B ===")
# Sử dụng S[1] = A * S[0] XOR B
s0 = states_bits[0]
s1 = states_bits[1]

# A * S[0]
a_times_s0 = gf2_matrix_multiply(A_recovered, s0)

# B = S[1] XOR (A * S[0])
B = [s1[i] ^ a_times_s0[i] for i in range(32)]
B_value = from_bits(B)

print(f"B (hex): {B_value:08x}")
print(f"B (dec): {B_value}")

print("\n=== Bước 3: Xác minh ===")
# Kiểm tra với state tiếp theo
errors = 0
for i in range(min(5, len(leaked_states) - 1)):
    s_current = states_bits[i]
    s_next_actual = states_bits[i + 1]
    
    # Tính S[n+1] = A * S[n] XOR B
    a_times_s = gf2_matrix_multiply(A_recovered, s_current)
    s_next_calc = [a_times_s[j] ^ B[j] for j in range(32)]
    
    if s_next_calc == s_next_actual:
        print(f"✓ State {i} -> {i+1}: Chính xác")
    else:
        print(f"✗ State {i} -> {i+1}: Sai")
        errors += 1

print("\n=== Bước 4: Tạo keystream và giải mã ===")
# Keystream = byte thấp nhất của mỗi state
keystream = bytes([s & 0xFF for s in leaked_states[:len(ciphertext)]])

print(f"Keystream ({len(keystream)} bytes): {keystream.hex()}")
print(f"Ciphertext ({len(ciphertext)} bytes): {ciphertext.hex()}")

# Giải mã
plaintext = bytes([c ^ k for c, k in zip(ciphertext, keystream)])

print(f"\n{'='*50}")
print(f"PLAINTEXT: {plaintext}")
print(f"{'='*50}")

# Thử decode
try:
    flag = plaintext.decode('ascii')
    print(f"\n🚩 FLAG: {flag}")
except:
    print(f"\nFlag (hex): {plaintext.hex()}")
    print(f"Flag (bytes): {plaintext}")