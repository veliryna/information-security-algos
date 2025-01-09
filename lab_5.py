# -*- coding: cp1251 -*-
from random import randint

def main():
    # Variant2 p, g
    g = 2
    p = 29

    raw_name = "ВЕЛИЧКО ІРИНА ЄВГЕНІВНА"
    text_input = raw_name.encode('cp1251')
    print("Message to encrypt: " + raw_name)

    # El-Gamal keys generation
    # private key
    x = randint(1, p - 2)
    PRIVATE_KEY = x
    print("Generated private key: ", PRIVATE_KEY)

    # public key
    h = pow(g, x) % p
    print("h: " + str(h))
    print("Generated public key: (" + str(p) + ',' + str(g) + ',' + str(h) + ')')

    # ENCRYPTION
    r = randint(1, p - 1)
    c1 = pow(g, r) % p
    encrypted_message_blocks = []
    encrypted_message = ''

    for m_block in text_input:
        '''
        m-blocks should be lesser then p. Because cp1251 codes for Ukrainian letters are 
        in 190-200 range, I split the message in 2 parts - separate m_block into two parts: 
        the left part (left) containing the four most significant bits, 
        and the right part (right) containing the four least significant bits.
        '''
        left = m_block >> 4
        right = m_block & 0b1111

        c_left = (left * pow(h, r)) % p
        encrypted_message_blocks.append([c1, c_left])
        encrypted_message += str(c1) + str(c_left)

        c_right = (right * pow(h, r)) % p
        encrypted_message_blocks.append([c1, c_right])
        encrypted_message += str(c1) + str(c_right)

    print("\nENCRYPTION.................")
    print("Encrypted message:  ", encrypted_message)

    # DECRYPTION
    i = 1
    s = 0
    decrypted_message_blocks = []
    decrypted_message = ''
    for c1, c2 in encrypted_message_blocks:
        m = (c2 * pow(c1, p - 1 - PRIVATE_KEY)) % p
        # recreation of initial m_block that was split
        if i % 2 == 1:
            s += m << 4
        else:
            s += m
            decrypted_message_blocks.append(str(s))
            decrypted_message += str(s)
        if i % 2 == 0:
            s = 0
        i += 1

    print("\nDECRYPTION.................")
    print("Decrypted message in cp1251 encoding:  ", decrypted_message)

    # DECODING
    r = []
    for d in decrypted_message_blocks:
        r.append(int(d))
    decoded = bytearray(r).decode('cp1251')
    print("Decoded message: ", decoded)

main()
