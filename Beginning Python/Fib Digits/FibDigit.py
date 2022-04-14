# -----------------------------------------------------
# Comparison of fibonacci number last digit calculators
# -----------------------------------------------------


from time import perf_counter
from math import log10, floor


def round_figs(x, sig):
    """
    Rounds float value to given significant figures
    Useful for solving discrepancies in per_counter()

    :param x: float value to round
    :param sig: number of significant figures to round to
    :return: rounded float value
    """
    return round(x, sig + 1 - int(floor(log10(abs(x)))))


def standard_fib(n) -> float:
    """
    Standard calculation of fibonacci numbers
    Prints the last digit of the nth fibonacci number

    :param n: nth fibonacci number to calculate
    :return: rounded benchmark speed of calculation in seconds
    """

    n1, n2 = 0, 1

    t1 = perf_counter()

    for _ in range(2, n):
        n3 = n1 + n2
        n1 = n2
        n2 = n3

    t2 = perf_counter()

    print(n2 % 10)
    return round_figs(t2 - t1, 2)


def mod_fib(n) -> float:
    """
    Calculates only the last digit of each fibonacci number
    Prints the last digit of the nth fibonacci number

    :param n: nth fibonacci number to calculate
    :return: rounded benchmark speed of calculation in ms
    """
    n1, n2 = 0, 1

    t1 = perf_counter()

    for _ in range(2, n):
        n3 = (n1 + n2) % 10
        n1 = n2
        n2 = n3

    t2 = perf_counter()

    print(n2)
    return round_figs(t2 - t1, 2)


def sequence_fib(n) -> float:
    """
    Calculates the last digit of the fibonacci number using a known sequence
    Prints the last digit of the nth fibonacci number

    :param n: nth fibonacci number to calculate
    :return: rounded benchmark speed of calculation in seconds
    """
    dig_list = (0, 1, 1, 2, 3, 5, 8, 3, 1, 4, 5, 9, 4, 3, 7, 0, 7, 7, 4, 1, 5, 6, 1, 7, 8, 5, 3, 8, 1, 9, 0,
                9, 9, 8, 7, 5, 2, 7, 9, 6, 5, 1, 6, 7, 3, 0, 3, 3, 6, 9, 5, 4, 9, 3, 2, 5, 7, 2, 9, 1, 0, 5)

    t1 = perf_counter()

    n2 = dig_list[n % 60 - 1]

    t2 = perf_counter()

    print(n2)
    return round_figs(t2 - t1, 2)


def main():
    n = 500_000  # Nth fibonacci number to calculate

    print("Standard: " + str(standard_fib(n)))
    print("Modulus: " + str(mod_fib(n)))
    print("Sequence: " + str(sequence_fib(n)))


if __name__ == '__main__':
    main()
