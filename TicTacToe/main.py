# Prints playing field
def print_field():
    print("   1 2 3\n"
          f"1  {Matrix[0][0]} {Matrix[0][1]} {Matrix[0][2]} \n"
          f"2  {Matrix[1][0]} {Matrix[1][1]} {Matrix[1][2]} \n"
          f"3  {Matrix[2][0]} {Matrix[2][1]} {Matrix[2][2]} \n")


# Tests for three in a row and prints victor
def test_win():
    for i in range(3):
        if Matrix[0][i] == Matrix[1][i] == Matrix[2][i] and Matrix[0][i] != "_":
            print(f"{Matrix[0][i]} wins")
            return True
    for i in range(3):
        if Matrix[i][0] == Matrix[i][1] == Matrix[i][2] and Matrix[i][0] != "_":
            print(f"{Matrix[i][0]} wins")
            return True
    if Matrix[0][0] == Matrix[1][1] == Matrix[2][2] or Matrix[0][2] == Matrix[1][1] == Matrix[2][0]:
        if Matrix[1][1] != "_":
            print(f"{Matrix[1][1]} wins")
            return True
    if turnCount == 9:
        print("Draw")
        return True
    return False


# Sets user input into matrix of playing field
def input_coordinates(t):
    while True:
        x1 = input(f"{t} turn. Input coordinates:\n")
        y1 = input()

        if not x1.isnumeric() or not y1.isnumeric():
            print("You should enter numbers!")
        elif not 1 <= int(x1) <= 3 or not 1 <= int(y1) <= 3:
            print("Coordinates should be from 1 to 3!")
        elif Matrix[int(x1) - 1][int(y1) - 1] != "_":
            print("This cell is occupied! Choose another one!")
        else:
            Matrix[int(y1) - 1][int(x1) - 1] = t
            break


# Prints instructions for play
def print_instructions():
    print("Simple Tic-Tac-Toe. Enter column then enter row when prompted for coordinates.")
    print("=" * 78)
    print()


# Declaring variables
Matrix = [["_" for x in range(3)] for y in range(3)]
turn = "X"  # X starts play
turnCount = 0

print_instructions()

# Loop takes turns playing the game
while not test_win():
    print_field()
    input_coordinates(turn)

    if turn == "X":
        turn = "O"
    else:
        turn = "X"

    turnCount += 1
