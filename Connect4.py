import copy

def print_board(board):
    print()
    string = ''
    for row in board:
        string+='+---+---+---+---+---+---+---+\n'
        for spot in row:
            string+='|'
            if spot == None:
                string+='   '
            else:
                string+=' '+str(spot)+' '
        string+='|\n'
    string+='+---+---+---+---+---+---+---+\n'
    print(string)
        
def check_win(board, piece, move):
    win_len = 4
    i = 0
    while board[i][move-1] == None:
        i += 1
    piece_count = 0
    for j in range(win_len):
        try:
            if board[i+j][move-1] == piece:
                piece_count += 1
        except IndexError:
            break
    if piece_count == win_len:
        return True
    for j in range(win_len-1, -1, -1):
        piece_count_1 = 0
        piece_count_2 = 0
        piece_count_3 = 0
        for k in range(win_len):
            if (i+j-k >= 0 and i+j-k < 6 and move-1-j+k >= 0 and move-1-j+k < 7
                and board[i+j-k][move-1-j+k] == piece):
                piece_count_1 += 1
            if (i+j-k >= 0 and i+j-k < 6 and move-1+j-k >= 0 and move-1+j-k < 7
                and board[i+j-k][move-1+j-k] == piece):
                piece_count_2 += 1
            if (i >= 0 and i < 6 and move-1+j-k >= 0 and move-1+j-k < 7
                and board[i][move-1+j-k] == piece):
                piece_count_3 += 1
        if piece_count_1 == win_len or piece_count_2 == win_len or piece_count_3 == win_len:
            return True
    return False
            
def check_full(board):
    for i in range(6):
        for j in range(7):
            if board[i][j] == None:
                return False
    return True

def find_value(board, depth, is_turn, piece, opp_piece, move):
    if depth == max_depth:
        return 0
    if check_win(board, piece, move):
        return max_depth + 1 - depth
    if check_win(board, opp_piece, move):
        return (max_depth + 1)*-1 + depth
    if check_full(board):
        return 0
    if is_turn:
        best_val = None
        for i in range(1, 8):
            temp_board = copy.deepcopy(board)
            if place_piece(temp_board, i, piece):
                value = find_value(temp_board, depth+1, False, piece, opp_piece, i)
                if best_val == None or value > best_val:
                    best_val = value
    else:
        best_val = None
        for i in range(1, 8):
            temp_board = copy.deepcopy(board)
            if place_piece(temp_board, i, opp_piece):
                value = find_value(temp_board, depth+1, True, piece, opp_piece, i)
                if best_val == None or value < best_val:
                    best_val = value
    del board
    return best_val

def find_place(board, piece, opp_piece):
    best_val = None
    best_move = None
    for i in range(1, 8):
        temp_board = copy.deepcopy(board)
        if place_piece(temp_board, i, piece):
            value = find_value(temp_board, 0, False, piece, opp_piece, i)
            if best_val == None or value > best_val:
                best_val = value
                best_move = i
    return best_move

def place_piece(board, col, piece):
    try:
        col = int(col)
    except TypeError:
        return False
    if col < 1 or col > 7:
        return False
    if board[0][col-1] != None:
        return False
    i = 5
    while board[i][col-1] != None:
        i -= 1
    board[i][col-1] = piece
    return True

def turn(is_human, board, piece, opp_piece):
    if is_human:
        user = input('Enter the column (1-7): ')
        while not place_piece(board, user, opp_piece):
            print('Invalid Input.')
        print_board(board)
        if check_win(board, opp_piece, int(user)):
            print(opp_piece+"'s win.")
            return
    else:
        print('Calculating...')
        move = find_place(board, piece, opp_piece)
        place_piece(board, move, piece)
        print_board(board)
        if check_win(board, piece, move):
            print(piece+"'s win.")
            return
    
    if check_full(board):
        print("Tie.")
        return
    turn((not is_human), board, piece, opp_piece)

max_depth = 5

if __name__ == '__main__':
    while True:
        board = [[None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None]]

        while True:
            try:
                max_depth = int(input('What depth would you like for the bot?\n'+
                                  '(Higher depth means a better bot but a longer calculation time)\n'+
                                  'The reccommended depth is 5. '))
                break
            except ValueError:
                print('Invalid input.')
                
        while True:
            start = input('Would you like to start? Enter Y for yes or N for no. ')
            if start.upper() == 'Y':
                print_board(board)
                turn(True, board, '2', '1')
                break
            elif start.upper() == 'N':
                turn(False, board, '1', '2')
                break
            print('Invalid input.')

        again = input('\nWould you like to play again? Enter Y for yes or N for no. ')
        print()
        if again.upper() == 'N':
            break
        elif again.upper() == 'Y':
            pass
        else:
            print('Invalid input.')
