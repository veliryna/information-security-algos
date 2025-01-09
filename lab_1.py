# -*- coding: cp1251 -*-
import binascii

MTK_2_ua = {
    "prefix": '00000',
    " ": '00100',
    "\n": '01000',
    "\r": '00010',
    "А": '11000',
    "Б": '10011',
    "В": '11001',
    "Г": '01011',
    "Д": '10010',
    "Е": '10000',
    "Ж": '01111',
    "И": '01100',
    "Й": '11010',
    "К": '11110',
    "Л": '01001',
    "М": '00111',
    "Н": '00110',
    "О": '00011',
    "П": '01101',
    "Р": '01010',
    "С": '10100',
    "Т": '00001',
    "У": '11100',
    "Ф": '10110',
    "Х": '00101',
    "Ц": '01110',
    "І": '10101',
    "Я": '11101',
}

MTK_2_digit = {
    "prefix": '11011',
    "З": '10000',
    "Є": '10110',
    "Ї": '10010',
    "Ч": '01010',
    "Ш": '01011',
    "Щ": '00101',
    "Ю": '11010',
}


def main():
    name = "ВЕЛИЧКО ІРИНА ЄВГЕНІВНА"

    # encode name in MTK_2 encoding
    mtk_2_text = []
    old_prefix = -1
    for letter in name:
        if letter in MTK_2_ua.keys():
            if old_prefix != MTK_2_ua.get("prefix"):
                old_prefix = MTK_2_ua.get("prefix")
                mtk_2_text.append(old_prefix)

            mtk_code = MTK_2_ua.get(letter)
            mtk_2_text.append(mtk_code)

        else:
            if old_prefix != MTK_2_digit.get("prefix"):
                old_prefix = MTK_2_digit.get("prefix")
                mtk_2_text.append(old_prefix)

            mtk_code = MTK_2_digit.get(letter)
            mtk_2_text.append(mtk_code)

    print("Name: " + name)
    print("Name in MTK-2 encoding: ", mtk_2_text)

    mtk_string = ''.join(mtk_2_text)
    four_bit_combos = [mtk_string[i:i + 4] for i in range(0, len(mtk_string), 4)]
    print("4-bit combinations: ", four_bit_combos)
    hex_text = "0x" + ''.join([hex(int(binary_string, 2))[2:] for binary_string in four_bit_combos])
    print("HEX TEXT: ", hex_text)
    ascii_encoded = []
    for code in four_bit_combos:
        ascii_encoded.append(chr(int(code, 2)))
    print("ASCII-encoded from MTK-2: ", ascii_encoded)
    name_to_ascii_hex = [binascii.hexlify(c.encode('cp1251')) for c in name]
    print("Name in ASCII encoding (hex): ", name_to_ascii_hex)
    name_to_ascii_bin = [bin(int.from_bytes(c.encode('cp1251'), byteorder='big')) for c in name]
    print("Name in ASCII encoding (bin): ", name_to_ascii_bin)

    # TASK 2
    key = 'ІРИНА'
    gamma = key.encode('cp1251')
    raw_text = 'ВЕЛИЧКО'
    message = raw_text.encode('cp1251')
    print('\n\nTASK 2: Gamma encryption')
    print('Gamma: ' + key)
    print('Message: ' + raw_text)

    # gamma-encryption
    encrypted = []
    subkey = 0
    s_encrypted = ''
    for c in message:
        if subkey == len(key):
            subkey = 0
        code = c ^ gamma[subkey]
        encrypted.append(code)
        s_encrypted += hex(code).lstrip('0x').zfill(2)
        subkey += 1
    print('ENCRYPTED MESSAGE: 0x' + s_encrypted)

    # gamma decryption
    subkey = 0
    decrypted = []
    s_decrypted = ''
    for code in encrypted:
        if subkey == len(key):
            subkey = 0
        code = code ^ gamma[subkey]
        decrypted.append(code)
        s_decrypted += hex(code).lstrip('0x').zfill(2)
        subkey += 1
    print('DECRYPTED MESSAGE: 0x' + s_decrypted)

    # decoding primary text after gamma-decryption
    decoded = bytearray(decrypted).decode('cp1251')
    print('Decoded Text: ' + decoded)


main()
