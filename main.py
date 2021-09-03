import random


def check_win(player):
    # Function for checking wining

    if (g_m[0][0] == g_m[0][1] == g_m[0][2] == ('X' or '0') or g_m[1][0] == g_m[1][1] == g_m[1][2] == ('X' or '0') or
        g_m[2][0] == g_m[2][1] == g_m[2][2] == ('X' or '0') or g_m[0][0] == g_m[1][0] == g_m[2][0] == ('X' or '0') or
        g_m[0][1] == g_m[1][1] == g_m[2][1] == ('X' or '0') or g_m[0][2] == g_m[1][2] == g_m[2][2] == ('X' or '0') or
        g_m[0][0] == g_m[1][1] == g_m[2][2] == ('X' or '0') or g_m[0][2] == g_m[1][1] == g_m[2][0] == ('X' or '0')):
        print(f'Player {player} wins the Game')
        return True
    elif all(['-' not in g_m[0], '-' not in g_m[1], '-' not in g_m[2]]):
        print('Withdraw')
        return True
    return False


def check_input(in_type, ch):
    # Function for checking correction of movement input

    item = in_type.split()
    error_message = 'Wrong input. Must be two digits (from 0 to 2) separated by space'
    parse_move = False
    while not parse_move:
        if len(item) != 2:
            print(error_message)
            item = input(f'{ch}. Your move: ').split()
        elif not (item[0].isdigit() and item[1].isdigit()):
            print(error_message)
            item = input(f'{ch}. Your move: ').split()
        elif not (0 <= int(item[0]) <= 2 and 0 <= int(item[1]) <= 2):
            print(error_message)
            item = input(f'{ch}. Your move: ').split()
        else:
            parse_move = True
    return tuple(int(i) for i in item)


def check_rules(move_to_check, ch):
    # Function for checking two rules

    dict_of_vars = {(g_m[0][0], g_m[0][1], g_m[0][2]): [(0, 0), (0, 1), (0, 2)],
                    (g_m[1][0], g_m[1][1], g_m[1][2]): [(1, 0), (1, 1), (1, 2)],
                    (g_m[2][0], g_m[2][1], g_m[2][2]): [(2, 0), (2, 1), (2, 2)],
                    (g_m[0][0], g_m[1][0], g_m[2][0]): [(0, 0), (1, 0), (2, 0)],
                    (g_m[0][1], g_m[1][1], g_m[2][1]): [(0, 1), (1, 1), (2, 1)],
                    (g_m[0][2], g_m[1][2], g_m[2][2]): [(0, 2), (1, 2), (2, 2)],
                    (g_m[0][0], g_m[1][1], g_m[2][2]): [(0, 0), (1, 1), (2, 2)],
                    (g_m[0][2], g_m[1][1], g_m[2][0]): [(0, 2), (1, 1), (2, 0)]}

    list_for_first_rule = []
    list_for_second_rule = []

    # Checking First Rule (if you can win - you have to win)

    for item, key in dict_of_vars.items():
        if all([item.count(ch) == 2, item.count('-') == 1]):
            list_for_first_rule.extend(key)
            print(list_for_first_rule)

    if len(list_for_first_rule) > 0:

        if move_to_check not in list_for_first_rule:
            print('You are bracking the first Rule. Please, end the game!')
            return False
        else:
            return True

    # Checking Second Rule (if you cannot win this turn,
    # but can lose next - you have prevent lose. If two losing position - check one)

    txt = '0' if ch == 'X' else 'X'
    for item, key in dict_of_vars.items():
        if all([item.count(txt) == 2, item.count('-') == 1]):
            list_for_second_rule.extend(key)

    if len(list_for_second_rule) > 0:
        if move_to_check not in list_for_second_rule:
            print('You are bracking the second Rule. Please, prevent end of this game')
            return False
        else:
            return True

    return True


def check_move(move_to_check):
    # Function that check movement if cell is occupied

    if g_m[move[0]][move[1]] == '-':
        return True
    else:
        print('Wrong cell. Choose another')
        return False


def make_move(move, ch):
    # Function to make move (check the cell with X or 0)

    g_m[move[0]][move[1]] = ch


def print_game():
    # Printing the game

    print('  0 1 2')
    for i, item in enumerate(g_m):
        print(i, *item)


def move_gen():
    # Generating next character

    iter_list = ['X', '0']
    while True:
        item = iter_list.pop(0)
        iter_list.append(item)
        yield item


g_m = []
quest = input('Do you want to play the game? (y/n) ').lower()

while quest not in 'yn':
    quest = input('Do you want to play the game? (y/n) ')

while quest == 'y':
    g_m = [['-' for _ in range(3)] for _ in range(3)]
    # g_m = [['X', '0', 'X'], ['-', 'X', '-'], ['-', '0', '-']]
    player1, player2 = (random.sample([input('Enter players 1 name: '),
                                       input('Enter players 2 name: ')], 2))
    players = {'X': player1, '0': player2}
    print(f'{player1} plays X, {player2} plays 0')
    move_type = move_gen()
    start_move = next(move_type)

    # Checking ending the game (win or draw)
    while not check_win(players[start_move]):

        # Printing empty game
        print_game()

        # Checking move input validity
        move = check_input(input(f'{players[start_move]}. Your move ({start_move}): '), players[start_move])

        # Checking empty cell or not
        while not check_move(move):
            move = check_input(input(f'{players[start_move]}. Your move ({start_move}): '), players[start_move])

        # Checking 2 rules
        while not check_rules(move, start_move):
            move = check_input(input(f'{players[start_move]}. Your move ({start_move}): '), players[start_move])

        # If everythig is OK, making move
        make_move(move, start_move)
        start_move = next(move_type)

    quest = input('Do you want to play one more game? (y/n) ')
