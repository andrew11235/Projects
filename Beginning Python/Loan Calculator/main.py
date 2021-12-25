import argparse
from math import floor, ceil, log


# Calculate principal
def calc_p():
    a = float(args.payment)  # Annuity payment
    n = int(args.periods)  # Periods (months)
    i = float(args.interest) / 1200  # Nominal interest rate
    p = floor(a / ((i * (i + 1) ** n) / ((i + 1) ** n - 1)))  # Calculate principal
    over = a * n - p  # Calculate overpayment
    print(f'Your load principal = {p}')
    print(f'Overpayment = {int(over)}' if over > 0 else '')


# Calculate periods
def calc_n():
    p = float(args.principal)  # Principal
    a = float(args.payment)  # Annuity payment
    i = float(args.interest) / 1200  # Nominal interest rate
    n = ceil(log(a / (a - i * p), i + 1))
    over = n * a - p
    years = n // 12
    months = n % 12
    print('It will take ', end='')
    print(f'{years} year{"s" if years > 1 else ""}{" and " if months > 0 else ""}' if years > 0 else '', end='')
    print(f'{months} months to repay this loan!' if months > 0 else ' to repay this loan')
    print(f'Overpayment = {floor(over)}' if over > 0 else '')


# Calculate payments
def calc_a():
    p = float(args.principal)  # Principal
    n = float(args.periods)  # Annuity payment
    i = float(args.interest) / 1200  # Nominal interest rate
    a = ceil(p * i * (1 + i) ** n / ((1 + i) ** n - 1))  # Calculate annuity payment
    over = ceil(a * n - p)  # Calculate overpayment
    print(f'Your monthly payment = {a}')
    print(f'Overpayment = {over}')


# Calculate differentiated payments
def calc_diff():
    p = float(args.principal)
    n = int(args.periods)
    i = float(args.interest) / 1200  # Nominal interest rate
    total = 0
    for m in range(1, n + 1):
        d = ceil(p / n + i * (p - p * (m - 1) / n))
        print(f'Month {m}: payment is {d}')
        total += d
    print(f'Overpayment = {int(total - p)}')


parser = argparse.ArgumentParser()
parser.add_argument("--type")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
parser.add_argument("--payment")
args = parser.parse_args()

vals = [args.principal, args.periods, args.interest, args.payment]

if vals.count(None) > 1 or any(float(n) < 0 for n in vals if n is not None):  # Ensure correct inputs
    print('Incorrect parameters')
    exit()

if args.type == "annuity":
    if args.principal is None:
        calc_p()

    elif args.periods is None:
        calc_n()

    elif args.payment is None:
        calc_a()

elif args.type == "diff":
    calc_diff()

else:
    print('Incorrect parameters')
