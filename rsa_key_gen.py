# Usage: Script.py create prime1 prime2
# Usage: Script.py break n e

import sys
import math

exponent_choices = [29, 23, 19, 17, 13, 7, 5, 3]

def calculate_d(phi, e):
    d = 1
    while (e*d) % phi != 1:
        d += 1
    return d

def create_pair():
    print(f'For primes: {numeric_arg1} {numeric_arg2}')
    n = numeric_arg1 * numeric_arg2
    phi = (numeric_arg1 - 1) * (numeric_arg2 - 1)
    e = 3
    for option in exponent_choices:
        if option < phi and math.gcd(option, phi) == 1:
            e = option
    d = calculate_d(phi, e)

    print(f'The smallest corresponding RSA key pair is: n={n}, e={e}, phi={phi}, d={d}')

def break_pair():
    print(f'For public key: n={numeric_arg1} and e={numeric_arg2}')
    digits_to_cut = int((math.log10(numeric_arg1) + 1) / 2) - 1
    print(digits_to_cut)
    divisor = pow(10, digits_to_cut)
    max_min = int(numeric_arg1 / divisor) + 1
    print(max_min)
    if max_min % 2 == 0:
        max_min -= 1
    current_guess = max_min
    while (numeric_arg1 % current_guess != 0) and current_guess > 1:
        current_guess -= 2
        if current_guess < 4:
            break
    if current_guess <= 1:
        print('Failed to find base primes.')
        exit()
    other_prime = numeric_arg1 / current_guess
    phi = (current_guess - 1)*(other_prime - 1)
    d = calculate_d(phi, numeric_arg2)
    print(f'The private key is: {d}. With base primes: {current_guess} and {other_prime}.')

if len(sys.argv) < 4:
    print('Supply at least 2 numeric arguments.')
    print('Usage Option 1: Script.py create prime1 prime2')
    print('Usage Option 2: Script.py break n e')
    exit()

action = sys.argv[1]
numeric_arg1 = int(sys.argv[2])
numeric_arg2 = int(sys.argv[3])

if action == 'create':
    create_pair()
elif action == 'break':
    break_pair()
else:
    print('Invalid action command.')
    print('Usage Option 1: Script.py create prime1 prime2')
    print('Usage Option 2: Script.py break n e')
    exit()
