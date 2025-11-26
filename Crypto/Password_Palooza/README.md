# Password Palooza
## Challange
- <Mang máng thôi không lưu đề>
- Đề cho một mã md5 có mã hex : 3a52fc83037bd2cb81c5a04e49c048a2
- Và gợi ý cho đây là hash của một mật khẩu phổ biến
- Kết thúc bằng 2 giá trị thập phân (digest)
## Solving
- Do mã tạo từ mật khẩu đơn giản nên chỉ cần hashcat và duyệt trong rockyou.txt (File sẵn của kali linux hoặc có thể down về)
- Lệnh thực hiện là:
```
    hashcat -a 6 -m 0 3a52fc83037bd2cb81c5a04e49c048a2 /usr/share/wordlists/rockyou.txt '?d?d'
```
- Trong đó: -m 0 là mode 0 hay mã hex dùng của md5, -a 6 là duyệt theo data trong file và có thêm mask phía sau (2 chữ số phía sau ) tức là '?d?d'.
- Mật khẩu nhận được: mr.krabbs57
- FLag là: pctf{mr.krabbs57}