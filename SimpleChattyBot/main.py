# Tests input for integer value
def int_input():
    while True:
        try:
            num = int(input())
            return num
        except:
            print("Invalid input. Try again.")


# Prints standard chatty bot greeting
def greet(bot_name, birth_year):
    print('Hello! My name is ' + bot_name + '.')
    print('I was created in ' + birth_year + '.')


# Takes input for name and prints a greeting with name
def remind_name():
    print('Please, remind me your name.')
    name = input()
    print('What a great name you have, ' + name + '!')


# Takes the remainders to calculate and print the user's age
def guess_age():
    print('Let me guess your age.')
    print('Enter remainders of dividing your age by 3, 5 and 7.')

    rem3 = int_input()
    rem5 = int_input()
    rem7 = int_input()
    age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105

    print("Your age is " + str(age) + "; that's a good time to start programming!")


# Loop to print integers up to the user's input
def count():
    print('Now I will prove to you that I can count to any number you want.')
    print("Enter the number to count to:")
    curr = 0
    num = int_input()
    while curr <= num:
        print(curr, '!')
        curr = curr + 1
    print()


# Prints multiple choice test that requires the correct input
def test():
    print("Let's test your programming knowledge.")
    print("What is the Python escape character?")
    print("1: 'e'\n2: '*'\n3: '\\'\n4: '#'")
    while int_input() != 3:
        print("Incorrect. Please try again.")
    print('Correct!')
    print()


# Prints ending statement
def end():
    print('Congratulations, have a nice day!')


greet('Aid', '2020')  # change it as you need
remind_name()
guess_age()
count()
test()
end()
