# -*- coding: cp1251 -*-
import random

PRIME_NUMBERS = []

def generate_prime_numbers():
    for i in range(2, 100):
        not_prime = 0
        for j in range(2, i // 2 + 1):
            if i % j == 0:
                not_prime = 1
                break
        if not_prime == 0:
            PRIME_NUMBERS.append(i)

def main():
    generate_prime_numbers()
    p = random.choice(PRIME_NUMBERS)
    q = random.choice(PRIME_NUMBERS)

    raw_name = "ВЕЛИЧКО ІРИНА ЄВГЕНІВНА"
    text_input = raw_name.encode('cp1251')
    print("Message to encrypt: " + raw_name)

    # RSA key generation
    print("p = " + str(p) + ", q = " + str(q))
    n = p * q
    print("n = " + str(n))
    euler_function = (p - 1) * (q - 1)
    print("Euler function value = " + str(euler_function))

    co_primes_array = []
    for i in range(3, euler_function, 2):
        not_co_primes = 0
        for j in range(PRIME_NUMBERS[0], i + 1):
            if i % j == 0 and euler_function % j == 0:
                not_co_primes = 1
                break
        if not_co_primes == 0:
            co_primes_array.append(i)

    e = random.choice(co_primes_array)
    print("e = " + str(e))

    # Euclid Algorithm to find d
    A = euler_function
    B = e
    T1 = 0
    T2 = 1
    while B != 0:
        Q = A // B
        R = A % B
        T = T1 - (T2 * Q)
        A = B
        B = R
        T1 = T2
        T2 = T

    d = T1
    if d < 0:
        d += euler_function

    print("d = " + str(d))
    print("\nRSA PUBLIC KEY: (" + str(e) + ", " + str(n) + ")")
    print("\nRSA PRIVATE KEY: (" + str(d) + ", " + str(n) + ")")

    # ENCRYPTION
    encrypted_message_array = []
    encrypted_message = ''
    for block in text_input:
        '''
        розбиваємо відкритий текст на блоки довжини менше log2(n) розрядів
        '''
        left = block >> 4
        right = block & 0b1111

        component = pow(left, e) % n
        encrypted_message_array.append(component)
        encrypted_message += str(component)

        component = pow(right, e) % n
        encrypted_message_array.append(component)
        encrypted_message += str(component)

    print("\nENCRYPTION.................")
    print("Encrypted message: " + encrypted_message)

    # DECRYPTION
    i = 1
    s = 0
    decrypted_message_array = []
    decrypted_message = ''
    for component in encrypted_message_array:
        x = pow(component, d) % n
        # join split block over 2 iterations
        if i % 2 == 1:
            s += x << 4
        else:
            s += x
            decrypted_message_array.append(str(s))
            decrypted_message += str(s)
        if i % 2 == 0:
            s = 0
        i += 1

    print("\nDECRYPTION.................")
    print("Decrypted message in cp1251 encoding:  ", decrypted_message)

    # DECODING
    r = []
    for d in decrypted_message_array:
        r.append(int(d))
    decoded = bytearray(r).decode('cp1251')
    print("Decoded message: ", decoded)


main()
