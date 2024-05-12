import random
import math

def generate_prime(lowerbound, upperbound):
    primes = []  # Initialize an empty list to store prime numbers

    # Iterate through the range from 'lower' to 'upper'
    for n in range(lowerbound, upperbound + 1):
        if n < 2:
            continue  # Skip numbers less than 2 (not prime)

        is_prime = True  # Assume 'n' is prime initially

        # Check for factors of 'n' by iterating from 2 to sqrt(n)
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                is_prime = False  # 'n' is not prime if it has a factor
                break

        if is_prime:
            primes.append(n)  # If 'n' is prime, add it to the 'primes' list

    if primes:
        p = random.choice(primes)  # Choose a random prime 'p' from 'primes'
        q = random.choice(primes)  # Choose another random prime 'q' from 'primes'
        return p, q
    else:
        return None, None  # Return None for 'p' and 'q' if no prime numbers were found

# Function to calculate the modular inverse using the Extended Euclidean Algorithm - calculates the decryption key
def modular_inverse(e, phi):
    if math.gcd(e, phi) != 1:
        return None  # e and phi should be relatively prime for a valid inverse
    u1, u2, u3 = 1, 0, e
    v1, v2, v3 = 0, 1, phi
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % phi

# Generate random prime numbers within the range [1, 50]
p, q = generate_prime(1, 50)

if p is not None and q is not None:
    print("p = ",p)
    print("q = ", q)
    n = p * q
    totient = (p - 1) * (q - 1)
    print("n = ", n)
    print("Totient = ", totient)

#choose a random factor of totient as the public exponent 'e'
    e = random.choice([prime for prime in range(2, totient) if totient % prime != 0])
    public_key = (e, n)

    print("Public Key (e, n) = ", public_key)

    # Calculate the decryption key 'd' using ed-1/totient = integer (whole number)
    d = modular_inverse(e, totient)

    if d is not None:
        private_key = (d, n)
        print("Private Key (d, n) = ", private_key)
    else:
        print("No valid modular multiplicative inverse found for the encryption key.")
else:
    print("No prime numbers found in the specified range")

message = 2

# Encrypt the message using the public key
ciphertext = message ** e % n

# Decrypt the ciphertext using the private key
decrypted_message = ciphertext ** d % n

print("Original message:", message)
print("Encrypted message (C):", ciphertext)
print("Decrypted message:", decrypted_message)



