import random
import lab_8_V

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

# array for all quadratic residues of modulo n
QUADRATIC_RESIDUES = []
# x^2 = a (mod n)
def calculate_quadratic_residues(n):
    for i in range(2, n - 1):
        a = (i * i) % n
        if a not in QUADRATIC_RESIDUES:
            QUADRATIC_RESIDUES.append(a)


# main program
def main():
    print("Iryna Velychko, group IP-03, journal number 92")
    print("TASK 1: RSA authentication protocol\n")

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

    # AUTHENTICATION
    # P sends to V public key (e,n)
    # V sends to P `x` after choosing r
    # P calculates and sends _r to V
    # V checks if _r = r. If true, then AUTHENTICATION is SUCCESSFUL, else FAILURE
    x = lab_8_V.get_rsa_public_key_and_send_x(e, n)
    _r = pow(x, d) % n
    print("r\' = " + str(_r))
    auth_result = lab_8_V.verify_r_value(_r)
    if auth_result == 1:
        print('AUTHENTICATION SUCCESSFUL')
    else:
        print('AUTHENTICATION FAILED')

    #############################
    #############################
    #############################
    #############################

    print("\n\nTASK 2: Fiat-Shamir authentication protocol\n")

    t = 1
    print("p = " + str(p) + ", q = " + str(q) + ", t = " + str(t))
    n = p * q
    print("n = " + str(n))

    calculate_quadratic_residues(n)
    co_primes = []
    for i in range(2, n - 1):
        not_co_primes = 0
        for j in range(PRIME_NUMBERS[0], i + 1):
            if i % j == 0 and n % j == 0:
                not_co_primes = 1
                break
        if not_co_primes == 0:
            # check if `i` is quadratic residue
            if i in QUADRATIC_RESIDUES:
                co_primes.append(i)

    s = random.choice(co_primes)
    v = (s * s) % n
    print("PUBLIC KEY: " + str(v))
    print("PRIVATE KEY: " + str(s))

    # AUTHENTICATION
    # P chooses random r, calculates and sends x (proof) to V
    r = random.randint(1, n - 1)
    print('r = ' + str(r))
    x = (r * r) % n
    print('x = ' + str(x))
    lab_8_V.get_proof_from_P(v, x)

    # V chooses random bit b
    b = lab_8_V.get_random_bit()
    print('random bit: ' + str(b))
    # P does one of two operations based on b value
    if b == 0:
        y = r
    else:
        y = r * s
    # P sends V the y value
    auth_result = lab_8_V.verify_fiat_shamir(y, n)
    if auth_result == 1:
        print('AUTHENTICATION SUCCESSFUL')
    else:
        print('AUTHENTICATION FAILED')


main()
