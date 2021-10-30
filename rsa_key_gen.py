import math
import sympy
import datetime

class RSA_key_gen:
    exponent_choices = [29, 23, 19, 17, 13, 7, 5, 3]

    n = 0
    d = 0
    e = 0
    
    test_ints = [0, 1, 2, 4, 3, 6, 7, 9, 16, 23, 512, 1024, 2056, 513, 112, 111, 100, 233]

    def __init__(self, min_prime_size=1, max_prime_size=100000000, *args, **kwargs):
        self.prime1 = sympy.randprime(min_prime_size, max_prime_size)
        self.prime2 = sympy.randprime(min_prime_size, max_prime_size)
        duplicates = 0
        while(self.prime2 == self.prime1):
            self.prime2 = sympy.randprime(min_prime_size, max_prime_size)
            duplicates += 1
            if duplicates > 4:
                print('Range invalid.')
                exit()

    def rsa_pair_is_valid(self):
        valid = True
        for test_int in self.test_ints:
            if test_int < self.n:
                cyper_text = pow(test_int, self.e, mod=self.n)
                plain_text = pow(cyper_text, self.d, mod=self.n)
                if test_int != plain_text:
                    valid = False
                    break
        return valid

    def calculate_d(phi, e):
        multiple = 1
        while (phi * multiple + 1) % e != 0:
            multiple += 1
        return (multiple * phi + 1) / e

    def create_pair(self):
        print(f'For primes: {self.prime1} {self.prime2}')
        self.n = self.prime1 * self.prime2
        phi = (self.prime1 - 1) * (self.prime2 - 1)
        self.e = 3
        for option in self.exponent_choices:
            if option < phi and math.gcd(option, phi) == 1:
                self.e = option
        self.d = RSA_key_gen.calculate_d(phi, self.e)
        print(f'The smallest corresponding RSA key pair is: n={self.n}, e={self.e}, phi={phi}, d={self.d}')
        self.d = int(self.d)
        print(f'Key is valid: {self.rsa_pair_is_valid()}')

    def break_pair(self):
        print(f'For public key: n={self.n} and e={self.e}')
        digits_to_cut = int((math.log10(self.n) + 1) / 2) - 1
        divisor = pow(10, digits_to_cut)
        max_min = int(self.n / divisor) + 1
        if max_min % 2 == 0:
            max_min -= 1
        current_guess = max_min

        start_search = datetime.datetime.now()
        prime_numbers = sympy.primerange(max_min)
        for prime in prime_numbers:
            if pow(self.n, 1, mod=prime) == 0:
                current_guess = prime
                break
        if current_guess == max_min:
            print('Failed to find base primes.')
            exit()
        print(f'Broke the primes in: {datetime.datetime.now() - start_search}')

        other_prime = self.n / current_guess
        phi = (current_guess - 1) * (other_prime - 1)
        private_key = RSA_key_gen.calculate_d(phi, self.e)
        print(f'The private key is: {private_key}. With base primes: {current_guess} and {other_prime}.')

# if len(sys.argv) < 2:
#     print('Supply at minimum an action argument.')
#     print('Options are "create", "break d e", "create_and_break".')
#     exit()
# action = sys.argv[1]

# key_gen = RSA_key_gen()

# if action == 'create':
#     print('Creating new RSA pair')
#     key_gen.create_pair()
# elif action == 'break':
#     print('Breaking inputted RSA pair')
#     key_gen.n = int(sys.argv[2])
#     key_gen.e = int(sys.argv[3])
#     key_gen.break_pair()
# elif action == 'create_and_break':
#     print('Creating and breaking RSA pair')
#     key_gen.create_pair()
#     key_gen.break_pair()
# else:
#     print('Invalid action command.')
#     print('Options are "create", "break d e", "create_and_break".')
#     exit()
