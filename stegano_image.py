from PIL import Image
import numpy as np
import random

def bitly(num):
    # Bitlify a number, e.g : 2 -> 00000010 or 6 -> 00000110
    if num <0 or num > 255:
        print("cant")
        return None
    x = bin(num)[2:]
    if len(x) < 8:
        x = '0'*(8-len(x)) + x
    return x

def numly(bit):
    # numlify an array representing a byte, e.g : [0,0,0,0,0,0,1,0] -> 2
    num = 0
    for i in range(len(bit)):
        num += bit[i] * (2**(len(bit)-i-1))
    return num


def placebit(arr, num, pos,end=False):
    x = bitly(num)
    posx, posy = pos
    dim = arr.shape
    if posx + 3 > dim[0]:
        posx = 0
        posy += 1
    for j in range(0,3):
        for i in range(0,3):
            if i==2 and j==2:
                if arr[posx][posy+i][i] % 2 == 0:
                    if not end:
                        arr[posx][posy + j][i] += 1
                else:
                    if end:
                        arr[posx][posy + j][i] += 1
            elif x[i+j*3] == '1':
                if arr[posx][posy + j][i] % 2 == 0:
                    arr[posx][posy + j][i] += 1
            else:
                if arr[posx][posy + j][i] % 2 == 1:
                    arr[posx][posy + j][i] += 1
    return arr


def stegano_encode(message, imarr):
    cx, cy = 0,0
    dim = imarr.shape
    for i in range(len(message)):
        ch = message[i]
        if i == len(message)-1:
            end=True
        else:
            end=False
        imarr = placebit(imarr,ord(ch),(cx,cy),end)
        cy += 3
        if cy+3 > dim[1]:
            cx += 1
            cy =0
    return imarr

def stegano_decode(imarr):
    arr = imarr.flatten()
    bits = []
    for i in range(0,len(arr),9):
        bits.append([0 if x % 2 == 0 else 1 for x in arr[i:i+8]])
#         print(arr[:9])
        if arr[i+8] % 2 == 0:
#             print(len(bits))
            # print(bits)
            break
    ret = [chr(numly(bit)) for bit in bits]
    strret = ""
    for i in ret:
        strret += i
    return strret
#     return bits

def placebitacak(arr, num, pos, end=False):
    x = bitly(num)
    posx, posy = pos
    dim = arr.shape
    if posx + 3 > dim[0]:
        posx = 0
        posy += 1
    print(f"{num} placed in {posx},{posy}")
    for j in range(0,3):
        for i in range(0,3):
            if end:
                if arr[posx][posy+i][j] % 2 == 0:
                    arr[posx][posy+i][j] += 1
            else:
                if i==2 and j==2:
                    if arr[posx][posy+i][i] % 2 == 1:
                        arr[posx][posy+i][i] += 1
                elif x[i+j*3] == '1':
                    if arr[posx][posy + j][i] % 2 == 0:
                        arr[posx][posy + j][i] += 1
                else:
                    if arr[posx][posy + j][i] % 2 == 1:
                        arr[posx][posy + j][i] += 1
    return arr

def stegano_acak(message, imarr):
    cx, cy = 0,0
    dim = imarr.shape
    for i in range(dim[0]):
        for j in range(dim[1]):
            if imarr[i][j][2] % 2 == 0:
                imarr[i][j][2] += 1
    for i in range(len(message)):
        ch = message[i]
#         if i == len(message)-1:
#             end=True
#         else:
#         end=False
        imarr = placebitacak(imarr,ord(ch),(cx,cy),False)
        cy += random.randint(1,5)*3
        if cy+3 > dim[1]:
            cx += 1
            cy = 0
        if i == len(message)-1:
            imarr = placebitacak(imarr,ord(ch),(cx,cy),True)
    return imarr

def stegano_acak_decode(imarr):
    arr = imarr.flatten()
    bits = []
    found = False
    for i in range(0,len(arr),9):
        x = [0 if x % 2 == 0 else 1 for x in arr[i:i+9]]
        if x[8] == 0:
            bits.append(x[:8])
#         print(arr[:9])
        if x[:8] == [1,1,1,1,1,1,1,1]:
#             print(len(bits))
#             print(bits)
            found = True
            break
    if not found:
        return []
    ret = [chr(numly(bit)) for bit in bits]
    strret = ""
    for i in ret:
        strret += i
    return strret

# CONTOH CARA PAKAI
if __name__=='__main__':
    imname = input("Masukkan nama file gambar : ")
    message = input("Masukkan pesan yang ingin anda sembunyikan : ")
    choice = True if input("Pilih, 1 = acak, 2 = sequensial") == 1 else False
    arr = np.array(Image.open(imname))
    if choice:
        hidden = stegano_acak(message,arr)
    else:
        hidden = stegano_encode(message,arr)
    Image.fromarray(hidden).save(input("Masukkan nama file untuk hasil hidden : "))

# DECODE
    # stegano_decode(hidden)
    # stegano_acak_decode(hidden)