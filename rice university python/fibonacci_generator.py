def iter_fib(fib, count):
    """
    generate the next 'count' fibonacci numbers
    """
    for iteration_count in range(count):
        fib.append(sum(fib[-2:]))
    return fib

print(iter_fib([0, 1], 10))
print(iter_fib([0, 1], 20))

