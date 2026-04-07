from PIL import Image

flag_im = Image.open("flag.png")
flag = flag_im.load()
lemur = Image.open("lemur.png").load()
# print(key)
for i in range(flag_im.size[0]):
    for j in range(flag_im.size[1]):
        # print(flag[i, j][0] ^ lemur[i, j][0])
        flag[i, j] = tuple(flag[i, j][k] ^ lemur[i, j][k] for k in range(3))
flag_im.save("out.png")
