from random import randint

def main():
    print("Iryna Velychko, group IP-03, journal number 92")
    print("Variant 2, g = 2, p = 29")
    print("TASK 1: Diffie-Hellman protocol key generation\n")

    g = 2
    p = 29

    # calculations for A and B
    xa = randint(1, p - 1)
    xb = randint(1, p - 1)
    print("xa = " + str(xa) + ", xb = " + str(xb))
    ya = pow(g, xa) % p
    yb = pow(g, xb) % p
    print("ya = " + str(ya) + ", yb = " + str(yb))
    A = pow(yb, xa) % p
    B = pow(ya, xb) % p
    private_key = pow(g, xa * xb) % p
    print("A = " + str(A) + ", B = " + str(B) + ", private key = " + str(private_key))
    print("\n\n")

    print("TASK 2: Name encryption/decryption\n")
    name = "ВЕЛИЧКО ІРИНА ЄВГЕНІВНА"
    print("Name: " + name)
    encrypted_result = ""
    for c in name:
        # take position of current letter from the `name`
        code = ord(c)
        # encrypt it by XOR cipher with calculated private key
        encrypted_code = code ^ private_key
        # convert position to letter
        encrypted_char = chr(encrypted_code)
        encrypted_result += encrypted_char
    print("Encrypted name: " + encrypted_result)

    decrypted_result = ""
    for c in encrypted_result:
        # take position of current letter from the encrypted `name`
        code = ord(c)
        decrypted_code = code ^ private_key
        # convert position to letter
        decrypted_char = chr(decrypted_code)
        decrypted_result += decrypted_char
    print("Decrypted name: " + decrypted_result)


main()
