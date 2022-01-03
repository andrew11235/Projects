from sys import setrecursionlimit

setrecursionlimit(10_000)


# Recursively finds a possible solution to the given board
def find_solution(y: int, x: int, moves: list, board_x: int, board_y: int):
    # Create list of valid moves at current position
    valid = []
    for y_diff, x_diff in (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1):
        # For each knight's move away, finds if the move is within bounds and not an already visited square
        y2, x2 = y + y_diff, x + x_diff
        if 0 <= y2 < board_y and 0 <= x2 < board_x and (y2, x2) not in [i[0] for i in moves if len(i) > 0]:
            valid.append((y2, x2))

    # Testing if the current path has reached a dead end with no further valid moves
    if len(valid) == 0:
        moves[-1].pop(0)

        # Removes trailing empty and single option paths in moves
        for i in range(len(moves) - 1, 0, -1):
            if len(moves[i]) <= 1:
                moves.pop(-1)
            else:
                break

        # Tests if program has tested all possible routes resulting in no solution
        if len(moves[0]) <= 1:
            return False

        # Removes first move in the furthest chain with multiple move options
        moves[-1].pop(0)

        # Tests further moves from a next back-tested position
        return find_solution(moves[-1][0][0], moves[-1][0][1], moves, board_x, board_y)

    # Sorts valid moves using Warnsdorff's rule (prioritizes testing paths with the least further moves)
    valid_dict = {}
    for m in valid:
        count = 0
        for y_diff, x_diff in (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1):
            y3, x3 = m[0] + y_diff, m[1] + x_diff
            if 0 <= y3 < board_y and 0 <= x3 < board_x:
                if (y3, x3) not in [i[0] for i in moves if len(i) > 0]:
                    count += 1

        # Forces known dead ends (0 further moves from that position) to be the last tested option
        if count == 0:
            count = 8

        valid_dict[m] = count

    valid_dict = {key: i for key, i in sorted(valid_dict.items(), key=lambda item: item[1])}

    # Appends sorted moves to the list of all moves
    moves.append([i for i in valid_dict])

    # Tests whether the list of current moves is a solution
    if len(moves) == board_x * board_y:
        # Returns the list of solution moves
        return [i[0] for i in moves]

    # Tests further moves from the current position (first coordinates in last index of moves)
    return find_solution(moves[-1][0][0], moves[-1][0][1], moves, board_x, board_y)


def main():
    # Prints instructions
    print("Knight's Tour: try visiting every square on the board or let the program find a solution.\n")

    # Sets board dimensions
    while True:
        board_input = input("Enter your board dimensions: ").split()

        try:
            board_x, board_y = int(board_input[0]), int(board_input[1])

            if len(board_input) != 2:
                raise IndexError
            if board_x < 1 or board_y < 1:
                raise IndexError

        except (ValueError, IndexError):
            print("Invalid dimensions!")

        else:
            break

    # Sets knight's starting position
    while True:
        start = input("Enter the knight's starting position: ").split()

        try:
            y, x = int(start[1]) - 1, int(start[0]) - 1
            if len(start) != 2:
                raise IndexError
            if not 1 <= x + 1 <= board_x or not 1 <= y + 1 <= board_y or len(start) != 2:
                raise IndexError

        except (ValueError, IndexError):
            print("Invalid dimensions!")

        else:
            break

    # Sets whether player want to play or view solution
    while True:
        setting = input("Do you want to try this puzzle? (y/n): ")

        if setting in ('y', 'n'):
            break

        print("Invalid input!")

    # Player plays the puzzle
    if setting == 'y':
        # Sets whether player wants hints
        while True:
            hint = input("Hints on? (y/n): ")

            if hint == "y":
                hint = True
                break

            elif hint == "n":
                hint = False
                break

            print("Invalid input!")

        p_len = len(str(board_x * board_y))  # Sets length of placeholder string used to format board
        board = [["_" * p_len for _ in range(int(board_x))] for _ in range(int(board_y))]  # Creates blank board
        board[y][x] = str(" " * (p_len - 1) + "X")  # Sets starting position of knight

        move_counter = 1

        while True:
            # Finds list of currently available moves
            valid = []

            for y_diff, x_diff in (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1):
                # For each knight's move away, finds if the move is within bounds and not an already visited square
                y2, x2 = y + y_diff, x + x_diff
                if 0 <= y2 < board_y and 0 <= x2 < board_x and "*" not in board[y2][x2]:
                    valid.append((y2, x2))
            if hint:
                # Calculates and replaces board squares to show the count of future available moves from each move
                for move in valid:
                    # For each available move, counts the future available moves from that square
                    count = -1  # Subtracting count of knight's current square
                    for y_diff, x_diff in (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1):
                        y3, x3 = move[0] + y_diff, move[1] + x_diff
                        if 0 <= y3 < board_y and 0 <= x3 < board_x and "*" not in board[y3][x3]:
                            count += 1

                    # Replaces board square to show the count of future available moves from that square
                    board[move[0]][move[1]] = str(" " * (p_len - 1) + str(count))

            # Prints current playing board
            border = f"{' ' if board_y < 10 else ' ' * 2}{'-' * (board_x * (p_len + 1) + 3)}"
            print(border)

            if board_y > 9:
                for i in range(len(board) - 1, -1, -1):
                    print(f"{' ' + str(i + 1) if i < 9 else i + 1}| {' '.join(board[i])} |")
            else:
                for i in range(len(board) - 1, -1, -1):
                    print(f"{i + 1}| {' '.join(board[i])} |")

            print(border)

            print(f"{' ' * (3 + p_len - 1)}{' ' if board_y >= 10 else ''}", end="")
            for i in range(board_x):
                print(str(i + 1), end=" " * (p_len - len(str(i + 2)) + 1))

            print("\n")

            # Tests if tour has ended
            if len(valid) == 0:
                if move_counter == board_x * board_y:
                    print("Tour complete")
                    break
                else:
                    print(f"No more possible moves. Your knight visited {move_counter} squares.")
                    break

            # Makes player move
            while True:
                move_input = input("Enter your next move: ").split()

                # Tests if player input move is valid
                try:
                    move_x, move_y = int(move_input[0]), int(move_input[1])

                    if (move_y - 1, move_x - 1) not in valid:
                        raise IndexError

                except (ValueError, IndexError):
                    print("Invalid move! ", end="")

                else:
                    for i in range(board_y):
                        for j in range(board_x):
                            board[i][j] = "_" * p_len if "*" not in board[i][j] else board[i][j]

                    board[y][x] = str(" " * (p_len - 1) + "*")
                    board[move_y - 1][move_x - 1] = str(" " * (p_len - 1) + "X")

                    y, x = move_y - 1, move_x - 1
                    break

            move_counter += 1

    # Computer prints the solution
    else:
        solution = find_solution(y, x, [[(y, x)]], board_x, board_y)

        if not solution:
            print("No solution exists!")

        else:
            print("\nSolution:")
            p_len = len(str(board_x * board_y))  # Sets length of placeholder string used to format board

            board = [["" for i in range(board_x)] for i in range(board_y)]

            for i, val in enumerate(solution):
                y_solution = int(val[0])
                x_solution = int(val[1])
                str_i = str(i)
                board[y_solution][x_solution] = str(f"{' ' * (p_len - len(str_i))}{str_i}")

            border = f"{' ' if board_y < 10 else ' ' * 2}{'-' * (board_x * (p_len + 1) + 3)}"
            print(border)

            if board_y > 9:
                for i in range(len(board) - 1, -1, -1):
                    print(f"{' ' + str(i + 1) if i < 9 else i + 1}| {' '.join(board[i])} |")
            else:
                for i in range(len(board) - 1, -1, -1):
                    print(f"{i + 1}| {' '.join(board[i])} |")

            print(border)

            print(f"{' ' * (3 + p_len - 1)}{' ' if board_y >= 10 else ''}", end="")
            for i in range(board_x):
                print(str(i + 1), end=" " * (p_len - len(str(i + 2)) + 1))

            print("\n")


if __name__ == '__main__':
    main()
