with open("output.txt", "r") as f:
    nums = list(int(i) for i in f.readline().strip()[1:-1].split(","))
s = ""
p = 1007621497415251
for i in nums:
    x = pow(i, (p-1)//2, p)

    s += "1" if x == 1 else "0"
print(s)
flag = ""
for i in range(len(s)//8):
    flag += chr(int(s[i*8:i*8+8], 2))
print(flag)
