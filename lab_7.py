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


# Euclidean Extended Algorithm
xx, yy = 0, 1
def gcd_extended(a, b):
    global xx, yy
    if a == 0:
        xx = 0
        yy = 1
        return b
    gcd = gcd_extended(b % a, a)
    x1 = xx
    y1 = yy
    xx = y1 - (b // a) * x1
    yy = x1
    return gcd


# Modular multiplicative inverse
def mod_inverse(A, M):
    g = gcd_extended(A, M)
    if g != 1:
        # in this case inverse does not exist
        return -1
    else:
        return (xx % M + M) % M


# main program
def main():
    print("Iryna Velychko, group IP-03, journal number 92")
    print("TASK 2: RSA electronic digital signature\n")

    # message creation
    M = ''
    for i in range(0, 4):
        M += hex(random.randint(0, 15)).lstrip('0x')
    print("INPUT MESSAGE: 0x" + M)

    generate_prime_numbers()
    # take 2-digit prime numbers for p and q
    while 1:
        p = random.choice(PRIME_NUMBERS)
        if p > 9:
            break
    while 1:
        q = random.choice(PRIME_NUMBERS)
        if q > 9:
            break

    print("p = " + str(p) + ", q = " + str(q))
    n = p * q
    print("n = " + str(n))
    euler_function = (p - 1) * (q - 1)
    print("Euler function value = " + str(euler_function))

    # odd random number e that is co-prime with euler_function and less than it
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
    # d is multiplicative inverse of e by modulo euler_function
    d = mod_inverse(e, euler_function)
    print("d = " + str(d))
    print("RSA PUBLIC KEY: (" + str(e) + ", " + str(n) + ")")
    print("RSA PRIVATE KEY: (" + str(d) + ", " + str(n) + ")")

    # calculate hash of message
    # h(M) = [(M^3 + 9)] mod (p-1)
    _M = int('0x' + M, 16)
    hash_M = (pow(_M, 3) + 9) % (p - 1)
    print("\nHASH: " + str(hash_M))

    # encryption with PRIVATE KEY
    S = pow(hash_M, d) % n
    print('MESSAGE AND SIGNATURE: (' + str(M) + ', ' + str(S) + ')')

    # verification of digital signature with PUBLIC KEY
    hash_to_verify = pow(S, e) % n
    print('DECRYPTED HASH: ' + str(hash_to_verify))

    if hash_to_verify == hash_M:
        print('SIGNATURE IS VERIFIED')
    else:
        print('ERROR: SIGNATURE IS NOT VERIFIED')

    ########################
    ########################
    ########################
    print("\n\nTASK 3: DSA electronic digital signature\n")

    # search for q that (p-1)=0 mod q
    _p = p - 1
    q = -1
    factors_of_p_minus_one = []
    for i in range(_p // 2, 1, -1):
        if _p % i == 0:
            if q == -1:
                q = i
            if i in PRIME_NUMBERS:
                factors_of_p_minus_one.append(i)

    print("INPUT MESSAGE: 0x" + M)
    print("p = " + str(p) + ", q = " + str(q))

    # search for primitive root g
    g = -1
    for j in range(2, _p):
        not_primitive_root = 1
        for i in factors_of_p_minus_one:
            if pow(j, _p // i) % p == 1:
                not_primitive_root = 0
                break
        if not_primitive_root == 1:
            g = j
            break
    print("Primitive root g modulo p: " + str(g))
    a = pow(g, _p // q) % p
    print("a = " + str(a))
    x = random.randint(1, q - 1)
    print("x = " + str(x))

    # public and private keys
    y = pow(a, x) % p
    print("y = " + str(y))
    print("PUBLIC KEY: (" + str(p) + ", " + str(g) + ", " + str(y) + ")")
    print("PRIVATE KEY: " + str(x))

    # calculate hash of message
    # h(M) = [(M^3 + 9)] mod (p-1)
    _M = int('0x' + M, 16)
    hash_M = (pow(_M, 3) + 9) % (p - 1)
    print("\nHASH: " + str(hash_M))

    # dsa digital signature creation
    r = 0
    s = 0
    while r == 0 or s == 0 or w == -1:
        k = random.randint(1, q - 1)
        r = (pow(a, k) % p) % q
        if r == 0:
            continue
        i = mod_inverse(k, q)
        if i == -1:
            continue
        s = (i * (hash_M + x * r)) % q
        if s == 0:
            continue
        w = mod_inverse(s, q)
        if w == -1:
            continue

    print('SIGNATURE: (' + str(r) + ', ' + str(s) + ')')

    # verification of digital signature
    if r <= 0 or r >= q:
        print('ERROR: SIGNATURE IS NOT VERIFIED')
    else:
        if s <= 0 or s >= q:
            print('ERROR: SIGNATURE IS NOT VERIFIED')
        else:
            u1 = (w * hash_M) % q
            u2 = (w * r) % q
            v = (pow(a, u1) * pow(y, u2) % p) % q
            print("v = " + str(v))
            if v == r:
                print('SIGNATURE IS VERIFIED')
            else:
                print('ERROR: SIGNATURE IS NOT VERIFIED')


main()
