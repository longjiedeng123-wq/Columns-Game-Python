def find_match(board: list[list['Field']]) -> None:
    'Find match attribute and change their state'
    _check_vertical(board)
    _check_horizontal(board)
    _check_left_diagonal(board)
    _check_right_diagonal(board)
    

def _check_match(list_c: list['Field']) -> None:
    'Update matching state of a list of field'
    for i in range(len(list_c) - 2):
        if list_c[i].attribute() != ' ':
            color1 = list_c[i].attribute()
            color2 = list_c[i + 1].attribute()
            color3 = list_c[i + 2].attribute()
            
            state1 = list_c[i].state()
            state2 = list_c[i + 1].state()
            state3 = list_c[i + 2].state()

            state_list = [state1, state2, state3]
            
            if color1 == color2 == color3 and\
               _valid_state(state_list):
                list_c[i].set_state('matching')
                list_c[i + 1].set_state('matching')
                list_c[i + 2].set_state('matching')
                
        
def _valid_state(states: list[str]) -> bool:
    'Returns true if colors has either matching or frozen state'
    valid = True
    for state in states:
        if state != 'matching' and state != 'frozen':
            valid = False

    return valid
              
def _check_vertical(board: list[list['Field']]) -> None:
    'Update the state of match color vertically'
    for col in board:
        _check_match(col)
    
                        
def _check_horizontal(board: list[list['Field']]) -> None:
    'Update the state of match color horizontally'
    for r in range(len(board[0])):
        row = []
        for c in range(len(board)):
            row.append(board[c][r])

        _check_match(row)

    
def _check_right_diagonal(board: list[list['Field']]) -> None:
    'Update the state of match color throughout right diagonal'
    for i in range(2, len(board[0])):
        row_i = i
        col_i = 0
        _add_and_check_right_diagonal(board, col_i, row_i)
        

    for i in range(1, len(board) - 2):
        col_i = i
        row_i = len(board[0]) - 1
        _add_and_check_right_diagonal(board, col_i, row_i)

    
def _check_left_diagonal(board: list[list['Field']]) -> None:
    'Update the state of match color throughout left diagonal'
    for i in range(2, len(board)):
        col_i = i
        row_i = len(board[0]) - 1
        _add_and_check_left_diagonal(board, col_i, row_i)

    for i in range(2, len(board[0])):
        col_i = len(board) - 1
        row_i = i
        _add_and_check_left_diagonal(board, col_i, row_i)
        


def _add_and_check_left_diagonal(board: list[list['Field']], col_i: int, row_i: int) -> None:
    'Adds up element in left diagonal and update their state if matching'
    left_diagonal = []
    while(row_i > -1 and col_i > -1):
        left_diagonal.append(board[col_i][row_i])
        col_i -= 1
        row_i -= 1
            
    _check_match(left_diagonal)
        

    
def _add_and_check_right_diagonal(board: list[list['Field']], col_i: int, row_i: int) -> None:
    'Adds up element in right diagonal and update their state if matching'
    right_diagonal = []
    while(row_i > -1 and col_i < len(board)):
        right_diagonal.append(board[col_i][row_i])
        col_i += 1
        row_i -= 1
            
    _check_match(right_diagonal)
        
