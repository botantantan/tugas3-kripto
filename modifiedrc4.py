def preprocess_hex(text) :
    preprocessed_text = ''

    i = 0
    while i < len(text) :
        if '\\x' == text[i:i+2] :
            c = int(text[i+2:i+4], base=16)
            preprocessed_text += chr(c)
            i += 4
        else :
            preprocessed_text += text[i]
            i += 1

    return preprocessed_text

def ksa(N, key_1, key_2) :
    if len(key_1) < 2 or len(key_2) < 2 :
        raise Exception("Keys must be at least 2 characters long")

    S1 = [i for i in range(N)]
    S2 = [(N-i-1) for i in range(N)]

    j1 = 0
    j2 = 0
    for i in range(N) :
        j1 = (j1 + S1[i] + ord(key_1[i % len(key_1)])) % N
        j2 = (j2 + S2[i] + ord(key_2[i % len(key_2)])) % N
        temp  = S1[i]
        S1[i] = S1[j1]
        S1[j1] = temp
        temp  = S2[i]
        S2[i] = S2[j1]
        S2[j1] = temp

    XOR = ''
    idx1 = idx2 = 0
    XOR += chr(ord(key_1[idx1 % len(key_1)]) ^ ord(key_2[idx2 % len(key_2)]))
    while idx1 != len(key_1)-1 or idx2 != len(key_2)-1 :
        idx1 = (idx1 + 1) % len(key_1)
        idx2 = (idx2 + 1) % len(key_2)
        XOR += chr(ord(key_1[idx1 % len(key_1)]) ^ ord(key_2[idx2 % len(key_2)]))

    j1 = 0
    j2 = 0
    for i in range(N//2) :
        j1 = ((j1 + S1[N//2-i-1]) ^ (ord(key_1[(N//2-i-1) % len(key_1)]) + ord(XOR[(N//2-i-1) % len(XOR)]))) % N
        j2 = ((j2 + S2[N//2-i-1]) ^ (ord(key_2[(N//2-i-1) % len(key_2)]) + ord(XOR[(N//2-i-1) % len(XOR)]))) % N
        temp  = S1[(N//2-i-1)]
        S1[(N//2-i-1)] = S1[j1]
        S1[j1] = temp
        temp  = S2[(N//2-i-1)]
        S2[(N//2-i-1)] = S2[j1]
        S2[j1] = temp

    for i in range(N//2, N) :
        j1 = ((j1 + S1[i]) ^ (ord(key_1[i % len(key_1)]) + ord(XOR[i % len(XOR)]))) % N
        j2 = ((j2 + S2[i]) ^ (ord(key_2[i % len(key_2)]) + ord(XOR[i % len(XOR)]))) % N
        temp  = S1[i]
        S1[i] = S1[j1]
        S1[j1] = temp
        temp  = S2[i]
        S2[i] = S2[j1]
        S2[j1] = temp

    j1 = j2 = 0
    for count in range(N) :
        i = count//2 if count % 2 == 0 else N-(count+1)//2
        j1 = (j1 + S1[i] + ord(key_1[i % len(key_1)])) % N
        j2 = (j2 + S2[i] + ord(key_2[i % len(key_2)])) % N
        temp  = S1[i]
        S1[i] = S1[j1]
        S1[j1] = temp
        temp  = S2[i]
        S2[i] = S2[j1]
        S2[j1] = temp

    return S1, S2

def prga(S1, S2, N, plaintext) :
    if len(plaintext) == 0 :
        raise Exception("Plaintext cannot be empty")

    keystream = ''
    i = 0
    j1 = 0
    j2 = 0
    for idx in range(len(plaintext)) :
        i = (i + 1) % N
        j1 = (j1 + S1[i]) % N
        j2 = (j2 + S2[i]) % N
        temp  = S1[i]
        S1[i] = S1[j1]
        S1[j1] = temp
        temp  = S2[i]
        S2[i] = S2[j1]
        S2[j1] = temp
        t = ((S1[i] + S1[j1]) + (S2[i] + S2[j2])) % N
        keystream += chr(S1[t] ^ S2[t])

    return keystream

def encrypt(plaintext, key_1, key_2) :
    N = 16
    if len(plaintext) == 0 :
        raise Exception("Plaintext should not be empty")
    if len(key_1) < 2 or len(key_2) < 2 :
        raise Exception("Keys must be at least 2 characters long")

    ciphertext = ''

    S1, S2 = ksa(N, key_1, key_2)
    keystream = prga(S1, S2, N, plaintext)
    for idx in range(len(plaintext)) :
        c = chr(ord(keystream[idx]) ^ ord(plaintext[idx]))
        ciphertext += c if c.isprintable() else r'\x{0:02x}'.format(ord(c))

    return ciphertext

def encrypt_binary(plaintext, key_1, key_2) :
    N = 16
    if len(plaintext) == 0 :
        raise Exception("Plaintext should not be empty")
    if len(key_1) < 2 or len(key_2) < 2 :
        raise Exception("Keys must be at least 2 characters long")

    ciphertext = []

    S1, S2 = ksa(N, key_1, key_2)
    keystream = prga(S1, S2, N, plaintext)
    for idx in range(len(plaintext)) :
        c = ord(keystream[idx]) ^ plaintext[idx]
        ciphertext.append(c)

    return ciphertext

def decrypt(ciphertext, key_1, key_2) :
    N= 16
    if len(ciphertext) == 0 :
        raise Exception("Ciphertext should not be empty")
    if len(key_1) < 2 or len(key_2) < 2 :
        raise Exception("Keys must be at least 2 characters long")

    ciphertext = preprocess_hex(ciphertext)

    plaintext = ''

    S1, S2 = ksa(N, key_1, key_2)
    keystream = prga(S1, S2, N, ciphertext)
    for idx in range(len(ciphertext)) :
        p = chr(ord(keystream[idx]) ^ ord(ciphertext[idx]))
        plaintext += p if p.isprintable() else r'\x{0:02x}'.format(ord(p))

    return plaintext

def decrypt_binary(ciphertext, key_1, key_2) :
    N = 16
    if len(ciphertext) == 0 :
        raise Exception("Ciphertext should not be empty")
    if len(key_1) < 2 or len(key_2) < 2 :
        raise Exception("Keys must be at least 2 characters long")

    plaintext = []

    S1, S2 = ksa(N, key_1, key_2)
    keystream = prga(S1, S2, N, ciphertext)
    for idx in range(len(ciphertext)) :
        p = ord(keystream[idx]) ^ ciphertext[idx]
        plaintext.append(p)

    return plaintext

a= encrypt("aku mau makan kokumi panggang", "helo","hobo")
print(a)
b = decrypt(a, "helo", "hobo")
print(b)
c= open('hello.txt', 'r') 
inp_file = bytearray(c.read(), encoding='utf8')
d= encrypt_binary(inp_file,  "helo", "hobo")
print(d)
f=decrypt_binary(d,  "helo", "hobo")
print(f)