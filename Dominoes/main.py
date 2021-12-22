from random import shuffle


# Prints the domino snake. Abridged when length is greater than 6.
def print_snake(s):
    if len(s) < 7:
        print(*s, sep="")
    else:
        print(f"{s[0]}{s[1]}{s[2]}...{s[-3]}{s[-2]}{s[-1]}")


# Requires user integer input.
def input_int(prompt, x_pieces):
    print(prompt)
    while True:
        m = input()
        try:
            m = int(m)
            if abs(m) > len(x_pieces):
                raise Exception
            return m
        except:
            print("Invalid input. Please try again.")


# Tests if the domino game has concluded
def test_end(s):
    if len(p_pieces) == 0:
        print("=" * 70)
        print(f"Stock size: {len(stock)}")
        print(f"Computer pieces: {len(c_pieces)}\n")
        print_snake(snake)
        print("\nYour pieces:")
        for i in range(len(p_pieces)):
            print(str(i + 1) + ":" + str(p_pieces[i]))
        print("Status: The game is over. You won!")
        return True
    elif len(c_pieces) == 0:
        print("=" * 70)
        print(f"Stock size: {len(stock)}")
        print(f"Computer pieces: {len(c_pieces)}\n")
        print_snake(snake)
        print("\nYour pieces:")
        for i in range(len(p_pieces)):
            print(str(i + 1) + ":" + str(p_pieces[i]))
        print("Status: The game is over. The computer won!")
        return True
    elif s[0][0] == s[-1][1] and sum([i.count(s[0][0]) for i in stock]) == 0:
        print("=" * 70)
        print(f"Stock size: {len(stock)}")
        print(f"Computer pieces: {len(c_pieces)}\n")
        print_snake(snake)
        print("\nYour pieces:")
        for i in range(len(p_pieces)):
            print(str(i + 1) + ":" + str(p_pieces[i]))
        print("Status: The game is over. It's a draw!")
        return True


# Creates total set of dominoes.
total = [[i, j] for i in range(7) for j in range(i, 7)]

# Assigns starting pieces, starting snake, and status of player to play first
while True:
    shuffle(total)
    stock, c_pieces, p_pieces = total[:14], total[14:21], total[21:28]
    p_double, c_double = -1, -1

    for i in p_pieces:
        if i[0] == i[1] and i[0] > p_double:
            p_double = i[0]
    for i in c_pieces:
        if i[0] == i[1] and i[0] > c_double:
            c_double = i[0]
    if p_double or c_double != -1:
        if p_double > c_double:
            status = "c"
            snake = [[p_double, p_double]]
            p_pieces.remove(snake[0])
        else:
            status = "p"
            snake = [[c_double, c_double]]
            c_pieces.remove(snake[0])
        break

# Prints playing field and makes computer and player moves
while True:
    print("=" * 70)
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(c_pieces)}\n")
    print_snake(snake)
    print("\nYour pieces:")
    for i in range(len(p_pieces)):
        print(str(i + 1) + ":" + str(p_pieces[i]))
    print()

    # Computer algorithm to make moves. Plays the highest value piece based on current number of alike in play.
    if status == "c":
        input("Status: Computer is about to make a move. Press Enter to continue...")
        value_counter = []  # Counts value of each number in play
        for i in range(7):
            value_counter.append(sum(x.count(i) for x in c_pieces) + sum(x.count(i) for x in snake))
        sort_pieces = []  # Sorts computer pieces based on value
        for i in range(len(c_pieces)):
            sort_pieces.append((i, value_counter[c_pieces[i][0]] + value_counter[c_pieces[i][1]]))
            sort_pieces.sort(key=lambda x: x[1], reverse=True)
        for p in sort_pieces:  # Tests each piece for play in order of value.
            piece = c_pieces[p[0]]
            if piece[0] == snake[0][0]:
                piece.reverse()
                snake.insert(0, piece)
                c_pieces.pop(p[0])
                break
            if piece[1] == snake[0][0]:
                snake.insert(0, piece)
                c_pieces.pop(p[0])
                break
            if piece[0] == snake[-1][1]:
                snake.append(piece)
                c_pieces.pop(p[0])
                break
            if piece[1] == snake[-1][1]:
                piece.reverse()
                snake.append(piece)
                c_pieces.pop(p[0])
                break

            if sort_pieces.index(p) == len(sort_pieces) - 1:  # Draws piece if no legal moves.
                if len(stock) > 0:
                    c_pieces.append(stock[0])
                    stock.pop(0)
                    break
        status = "p"

    # Takes user player move.
    else:
        move = input_int("Status: It's your turn to make a move. Enter your command: ", p_pieces)
        while True:
            if move == 0:
                if len(stock) > 0:
                    p_pieces.append(stock[0])
                    stock.pop(0)
                    break
                else:
                    pass
            else:
                if move < 0:
                    move = abs(move)
                    if p_pieces[move - 1][0] == snake[0][0]:
                        p_pieces[move - 1].reverse()
                        snake.insert(0, p_pieces[move - 1])
                        p_pieces.pop(move - 1)
                        break
                    elif p_pieces[move - 1][1] == snake[0][0]:
                        snake.insert(0, p_pieces[move - 1])
                        p_pieces.pop(move - 1)
                        break
                else:
                    if p_pieces[move - 1][1] == snake[-1][1]:
                        p_pieces[move - 1].reverse()
                        snake.append(p_pieces[move - 1])
                        p_pieces.pop(move - 1)
                        break
                    elif p_pieces[move - 1][0] == snake[-1][1]:
                        snake.append(p_pieces[move - 1])
                        p_pieces.pop(move - 1)
                        break
            move = input_int("Illegal move. Please try again.", p_pieces)
        status = "c"

    if test_end(snake):
        break
