
with open("input.txt", "r") as f:
    lines = f.readlines()
    p = int(lines[0].split("=")[-1])
    ints = list(int(i) for i in lines[2].split("=")[-1][2:-2].split(","))

for i in ints:
    leg = pow(i, (p-1)//2, p)
    if leg == 1:
        print(i)
        r = pow(i, (p+1)//4, p)
        print(max(r, (-r) % p))