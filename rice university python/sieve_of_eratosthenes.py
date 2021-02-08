"""
Implement the Sieve of Eratosthenes
https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
"""
import textwrap
import timeit

wrapper = textwrap.TextWrapper(width=80)


def compute_primes(bound):
    """
    Return a list of the prime numbers in range[2, bound]
    """
    lst_numbers = list(range(2, bound + 1))
    prime_status = [True] * (bound + 1)
    # checking for primality a different problem than generating list of primes
    # so assume all numbers in list are primes, until proven False
    # prime_status[index] stores the primality of lst_numbers[index]
    lst_primes = []  # returned list of prime numbers
    for divisor in lst_numbers:
        if prime_status[divisor]:
            lst_primes.append(divisor)
            for factor in range(divisor ** 2, bound + 1, divisor):
                # during each iteration of outer loop all factors of divisor will be marked as not prime (False)
                prime_status[factor] = False
    return lst_primes


def get_primes_lst(bound):
    lst_primes = compute_primes(bound)
    return lst_primes


num_of_primes = 10000000
start_time = timeit.default_timer()
lst_primes = get_primes_lst(num_of_primes)
print("time to generate", num_of_primes, "prime numbers", timeit.default_timer() - start_time)
print("there are ", len(lst_primes), "primes in the first ", num_of_primes, "numbers")

# for elm in wrapper.wrap(str(lst_primes)):
#      print(elm)
