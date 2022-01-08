from random import randint, choice


def main():
    count = 0

    # User chooses between level choices
    while True:
        level = input("Which level do you want? Write a number:\n"
                      "1- simple operations with numbers 2-9\n"
                      "2- integral squares of 11-29\n")
        if level not in ["1", "2"]:
            print("Incorrect format.")
        else:
            break

    # Gives 5 expressions to solve using +, -, * operations and numbers 2-9
    if level == "1":
        for _ in range(5):
            num1, num2 = randint(2, 9), randint(2, 9)

            op = choice(["+", "-", "*"])

            print(f"{num1} {op} {num2}")

            while True:
                answer = input()

                try:
                    answer = int(answer)
                except ValueError:
                    print("Incorrect format.")
                else:
                    break

            if answer == eval(f"{num1} {op} {num2}"):
                print("Right!")
                count += 1

            else:
                print("Wrong!")

    # Gives 5 integral squares to solve with numbers 11-29
    else:
        for _ in range(5):
            num1 = randint(11, 29)

            print(num1)

            while True:
                answer = input()

                try:
                    answer = int(answer)
                except ValueError:
                    print("Incorrect format.")
                else:
                    break

            if answer == pow(num1, 2):
                print("Right!")
                count += 1

            else:
                print("Wrong!")

    # Saves the result with a name to file "results.txt"
    save = input(f"Your mark is {count}/5. Would you like to save this result? Enter yes or no.")

    if save in ["yes", "YES", "y", "Yes"]:
        name = input("What is your name?")
        with open("results.txt", "a") as results:
            if level == 1:
                results.write(f"{name}: {count}/5 in level 1 (simple operations with numbers 2-9)")
            else:
                results.write(f"{name}: {count}/5 in level 2 (integral squares of 11-29)")
        print("The results are saved in \"results.txt\".")


if __name__ == '__main__':
    main()
