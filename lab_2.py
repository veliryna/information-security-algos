# -*- coding: cp1251 -*-

# ENCRYPT LOOP
ENCRYPT_LOOP = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0]
# DECRYPT LOOP
DECRYPT_LOOP = [0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0, 7, 6, 5, 4, 3, 2, 1, 0, 7, 6, 5, 4, 3, 2, 1, 0]

# X key
X = [0x80000080, 0x80000800, 0x80008000, 0x80000008, 0x80080000, 0x80800000, 0x80000000, 0x00000080]

# K key
rows = 8
cols = 16
K = (
    (0xA, 0x1, 0xE, 0x7, 0x0, 0xB, 0x9, 0xA, 0xA, 0x1, 0xE, 0x7, 0x0, 0xB, 0x9, 0xA),
    (0x1, 0xE, 0x7, 0x0, 0xB, 0x9, 0xA, 0xA, 0x1, 0xE, 0x7, 0x0, 0xB, 0x9, 0xA, 0xA),
    (0xE, 0x7, 0x0, 0xB, 0x9, 0xA, 0xA, 0x1, 0xE, 0x7, 0x0, 0xB, 0x9, 0xA, 0xA, 0x1),
    (0x7, 0x0, 0xB, 0x9, 0xA, 0xA, 0x1, 0xE, 0x7, 0x0, 0xB, 0x9, 0xA, 0xA, 0x1, 0xE),
    (0x0, 0xB, 0x9, 0xA, 0xA, 0x1, 0xE, 0x7, 0x0, 0xB, 0x9, 0xA, 0xA, 0x1, 0xE, 0x7),
    (0xB, 0x9, 0xA, 0xA, 0x1, 0xE, 0x7, 0x0, 0xB, 0x9, 0xA, 0xA, 0x1, 0xE, 0x7, 0x0),
    (0x9, 0xA, 0xA, 0x1, 0xE, 0x7, 0x0, 0xB, 0x9, 0xA, 0xA, 0x1, 0xE, 0x7, 0x0, 0xB),
    (0xA, 0xA, 0x1, 0xE, 0x7, 0x0, 0xB, 0x9, 0xA, 0xA, 0x1, 0xE, 0x7, 0x0, 0xB, 0x9),
)

def process(data_to_process, key_index, direction):
    print("LOOP " + str(key_index))

    # Preparing for Step 1
    print("INPUT : " + hex(data_to_process), )
    LEFT = data_to_process >> 32
    RIGHT = data_to_process & (pow(2, 32) - 1)
    print("Step 0.0: " + hex(LEFT) + " " + hex(RIGHT) + " <= LEFT & RIGHT PART")

    if direction == "ENCRYPT":
        x_num = ENCRYPT_LOOP[key_index]
        PART1 = RIGHT
        PART2 = LEFT
        PART1_DESC = "RIGHT"
        PART2_DESC = "LEFT"
    else:
        x_num = DECRYPT_LOOP[key_index]
        PART1 = LEFT
        PART2 = RIGHT
        PART1_DESC = "LEFT"
        PART2_DESC = "RIGHT"

    Xi = X[x_num]

    # 1 Step
    H = PART1 ^ Xi
    print("Step 1.0: " + hex(H) + " <= " + PART1_DESC + " ^ KEY X[" + str(x_num) + "]")

    # 2 Step - Replacement
    R = []
    n = 0
    s = ""
    # break on tetrads
    while n < 32:
        mask = 0b1111 << n
        x = (H & mask) >> n
        R.append(x)
        s += hex(x).lstrip('0x').zfill(1) + " "
        n += 4
    print("Tetrads:  " + s)

    # replace and make new 32 bit word
    HR = []
    word = ""
    for n in range(7, -1, -1):
        tetrad = R[n]
        new_val = K[n][tetrad]
        HR.append(new_val)
        word += hex(HR[7 - n]).lstrip('0x').zfill(1) + " "
    print("Step 2.0: " + word + " AFTER REPLACE")

    word = word.replace(' ', '')
    word = int("0x" + word, 16)

    # 3 Step - Shift left with loop
    S3 = ((word >> 11) | (word << (32 - 11))) & 0xFFFFFFFF
    print("Step 3.0: " + hex(S3) + " <= Step 2 << 11", 1)

    # 4 Step - XOR
    S4 = S3 ^ PART2
    print("Step 4.0: " + hex(PART2) + " <= " + PART2_DESC)
    print("Step 4.1: " + hex(S4) + " <= S3 ^ " + PART2_DESC)

    # 5 Step - S4 => right part, RIGHT => left part
    if direction == "ENCRYPT":
        # 5 Step - S4 => right part, RIGHT => left part
        S5 = hex(PART1).lstrip('0x').zfill(8) + " " + hex(S4).lstrip('0x').zfill(8)
    else:
        # 5 Step - S4 => left part, LEFT => right part
        S5 = hex(S4).lstrip('0x').zfill(8) + " " + hex(PART1).lstrip('0x').zfill(8)

    print("Step 5.0: " + S5 + " <= NEW LEFT & RIGHT")
    S5 = S5.replace(' ', '')

    return int('0x' + S5, 16)


def main():
    raw_name_full = "ВЕЛИЧКОІРИНА"
    raw_name_full_part = raw_name_full[:8]
    message = raw_name_full_part.encode('cp1251')
    print("Message to encrypt: " + str(raw_name_full_part))

    message_bitview = ""
    for n in message:
        message_bitview += hex(n).lstrip('0x').zfill(2)
    H_to_encrypt = int('0x' + message_bitview, 16)
    print("Message in bit view: " + hex(H_to_encrypt))

    # parameters
    s = ""
    for n in X:
        s += hex(n).lstrip('0x').zfill(8) + " "
    print("Session key (X): " + s)

    print("Replacement Block (K): ")
    n = 0
    for i in range(rows):
        s = str(n) + ": "
        for j in range(cols):
            s += hex(K[i][j]).lstrip('0x').zfill(1) + " "
        print(s)
        n += 1

    OUTPUT = H_to_encrypt

    # ENCRYPTION
    # LOOP 32-3
    for num in range(0, len(ENCRYPT_LOOP)):
        OUTPUT = process(OUTPUT, num, "ENCRYPT")

    s_encrypted = OUTPUT
    print("\nENCRYPTION:\n", 1)
    print(raw_name_full_part + " is encrypted to " + hex(s_encrypted) + "\n")

    # DECRYPTION
    # LOOP 32-P
    OUTPUT = s_encrypted
    for num in range(0, len(DECRYPT_LOOP)):
        OUTPUT = process(OUTPUT, num, "DECRYPT")

    s_decrypted = OUTPUT
    print("\nDECRYPTION:\n")
    print("" + hex(s_encrypted) + " is decrypted to " + hex(s_decrypted) + "\n")

    # parse hex result to byte array to decode it from cp1251
    H_to_decode = hex(s_decrypted).lstrip('0x').zfill(16)
    x = 0
    r = []
    for n in range(0, 8):
        ch = int("0x" + H_to_decode[x:x + 2], 16)
        x += 2
        r.append(ch)

    decoded = bytearray(r).decode('cp1251')
    print("Result decoded to: " + decoded)


main()
