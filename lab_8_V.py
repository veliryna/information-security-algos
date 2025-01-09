import random

###
# Functions for RSA authentication verification
###

r = 0
def get_rsa_public_key_and_send_x(e, n):
    global r
    # V chooses random r [1...n-1]
    r = random.randint(1, n - 1)
    x = pow(r, e) % n
    print('x = ' + str(x))
    # V sends to P `x`
    return x

# V checks if _r from P equals r
def verify_r_value(val):
    global r
    print('Checking if r\' = r: ', val, r)
    if val == r:
        return 1
    else:
        return -1


###
# Functions for Fiat-Shamir protocol
###

public_key = 0
bit = 0
proof = 0


def get_random_bit():
    global bit
    bit = random.randint(0, 1)
    return bit


def get_proof_from_P(publickey_val, proof_val):
    global public_key, proof
    public_key = publickey_val
    proof = proof_val


def verify_fiat_shamir(val, n):
    global public_key, bit, proof
    x1 = (val * val) % n
    x2 = (proof * pow(public_key, bit)) % n
    print('Checking if y^2 = x*v^b: ', x1, x2)
    if x1 == x2:
        return 1
    else:
        return -1
