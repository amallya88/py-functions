def collatz_generator(n):
    while True:
        # collatz function
        if n % 2 == 0:  # previous value was even
            n = n // 2
        else:  # previous value was odd
            n = 3 * n + 1
        yield n  # next value in sequence


# return the total stopping time and the sequence
def generate_collatz_seq(n):
    if n <= 0:
        raise ValueError("n should be non-zero positive integer")
    gen = collatz_generator(n)
    seq = [n]
    while True:
        try:
            nxt_int = next(gen)
            if nxt_int == 1:
                gen.close()
        except StopIteration:
            break
        seq.append(nxt_int)
    return seq


for n in range(1, 1001):
    collatz_seq = generate_collatz_seq(n)
    print("n={}, stopping time={}".format(n, len(collatz_seq)))
