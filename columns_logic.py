import copy
import match_logic

class NotIntError(Exception):
    'Raises when the value is not integer'
    pass

class InvalidRowError(Exception):
    'Raises when input row is invalid'
    pass

class InvalidColumnError(Exception):
    'Raises when input column is invalid'
    pass

class InvalidColorError(Exception):
    'Raises when color is invalid'
    pass

class InvalidStateError(Exception):
    'Raises when the state of color or state of space is invalid'
    pass

class InvalidFallerLocationError(Exception):
    'Raises when the faller is not on the board'
    pass

class InvalidContentFormatError(Exception):
    '''
    Raises when format of content is invalid,
    (it is invalid when number of lines of contents does not equal to
    number of row of the board or the number of characters in each line
    does not equal to the number of column of the board)
    '''
    pass

class ColumnFullError(Exception):
    'Raises when trying to generate a faller at a full column'
    pass

class GameOver(Exception):
    'Raises when faller do not fully show on the board'
    pass

class EndGame(Exception):
    'Raises when game ends'
    pass

class Field:
    def __init__(self, attribute: str, state: str):
        _check_field(attribute, state)
        self._attribute = attribute
        self._state = state

    def attribute(self) -> str:
        return self._attribute

    def state(self) -> str:
        return self._state

    def set_attribute(self, attribute: str) -> None:
        'Change attribute if it is valid'
        if attribute == ' ' or _check_color(attribute):
            self._attribute = attribute

    def set_state(self, state: str) -> None:
        'Changes state if it is valid'
        if state == 'empty' or _check_state(state):
            self._state = state
           
    
class Faller:
    def __init__(self, col: int, c0: Field, c1: Field, c2: Field):
        _check_int(col)
        self._fields = [c0, c1, c2]
        self._colors = [c0.attribute(), c1.attribute(), c2.attribute()]
        self._col = col
        self._row = 0

    def colors(self) -> list[str]:
        return self._colors

    def fields(self) -> list[Field]:
        return self._fields

    def row(self) -> int:
        return self._row

    def col(self) -> int:
        return self._col
    
    def set_state(self, state: str) -> None:
        'Set the state of the fields'
        for field in self._fields:
            field.set_state(state)

    def set_row(self, row: int) -> None:
        'The row is the row of bottom field in the faller'
        self._row = row

    def set_col(self, col: int) -> None:
        'Set the column of the faller'
        self._col = col

    def rotates(self) -> None:
        '''
        Changes the order of field by shifting them to the right.
        The right most element shift to the leftmost spot
        '''
        last_c = self._fields.pop()
        self._fields.insert(0, last_c)

    def can_rotate(self) -> bool:
        'Returns whether faller can be rotate'
        for field in self.fields():
            if field.state() != 'landing' and field.state() != 'falling':
                return False

        return True

    
    def has_match(self) -> bool:
        '''
        Returns true if any of field in the faller has matching state
        Returns False otherwise
        '''
        for field in self._fields:
            if field.state() == 'matching':
                return True
        return False

    def num_match(self) -> int:
        'Returns the number of match field in the faller'
        match_count = 0
        for field in self._fields:
            if field.state() == 'matching':
                match_count += 1

        return match_count

    def num_space(self) -> int:
        'Returns the number of space in the faller'
        space_count = 0
        for field in self._fields:
            if field.attribute() == ' ':
                space_count += 1

        return space_count

          
class ColumnsState:
    def __init__(self, row: int, column: int):
        self._row = row
        self._column = column
        self._faller = None
        _check_size_validity(row, column)
        self._board = []
        self._build_board(self._board, row, column)

    def row(self) -> int:
        return self._row

    def column(self) -> int:
        return self._column

    def faller(self) -> Faller:
        return self._faller

    def board(self) -> list[list[Field]]:
        return self._board
    
    def _set_faller(self, faller: Faller) -> None:
        'Assign a faller to the columns state only if there is no other faller'
        self._faller = faller

    def has_faller(self) -> bool:
        'Return true if there is a faller presented, false otherwise'
        for col in self._board:
            for field in col:
                if field.state() == 'falling' or field.state() == 'landing':
                    return True

        return False

    def create_faller(self, faller: Faller) -> None:
        'Creating a faller and update the board with tail color of the faller'
        f_col = faller.col()
        f_row = faller.row()
        _check_faller_location(self._column, self._row, f_col, f_row)
        _check_column_full(faller, self._board)
        if not self.has_faller():
            self._set_faller(faller)
            self._board[faller.col()][0] = faller.fields()[2]
            
        self._check_land(faller)

    def rotate_faller(self, faller: Faller) -> None:
        'Rotates and update the rotate faller field on the board'
        if faller:
            if faller.can_rotate():
                faller.rotates()
                f_col = faller.col()
                f_row = faller.row()
                i = 2
                for b_row in range(f_row, f_row - 3, -1):
                    if b_row > -1:
                        self._board[f_col][b_row] = faller.fields()[i]
                        i -= 1

            
    def _build_board(self, board: list, row: int, column: int) -> None:
        'Builds the rectangle board of field objects with column major'
        for c in range(column):
            column_list = []
            for r in range(row):
                column_list.append(Field(' ', 'empty'))
            self._board.append(column_list)
        
    
    def attribute_board(self) -> list[list[str]]:
        'Returns the board with attribute(color letter) only'
        attribute_board = copy.deepcopy(self._board)
        for i in range(len(attribute_board)):
            for j in range(len(attribute_board[i])):
                attribute_board[i][j] = self._board[i][j].attribute()

        return attribute_board
                
    
    def fill_contents(self, contents: list[str]) -> None:
        '''
        Takes a string of contents and checks it's validity,
        if it is invalid, raises an InvalidContentError
        else, update the state of the board with appropriate content
        '''
        _check_content_validity(contents, self._row, self._column)
        for r in range(len(contents)):
            for c in range(len(contents[r])):
                content = contents[r][c] 
                if content != ' ':
                    self._board[c][r].set_attribute(content)
                    self._board[c][r].set_state('frozen')

        self.apply_gravity()
        
        
    def _find_last_space_index(self, column: list[Field]) -> int:
        'Finds the last index of the ' ' space in a column'
        for i in range(len(column)-1,-1,-1):
            if column[i].attribute() == ' ':
                return i
        

    def find_match(self) -> None:
        'Label all the field with matched color'
        match_logic.find_match(self._board)


    def has_match(self) -> bool:
        'Returns whether a board has match element or not'
        for col in self._board:
            for field in col:
                if field.state() == 'matching':
                    return True
        return False


    def remove_match(self) -> None:
        'Removes all the field with matched colors'
        for col in self._board:
            for row in col:
                if row.state() == 'matching':
                    row.set_attribute(' ')
                    row.set_state('empty')


    def apply_gravity(self) -> None:
        'Applies gravity to all field'
        for i in range(len(self._board)):
            color_fields = []
            for j in range(len(self._board[i])):
                field = self._board[i][j]
                if field.attribute() != ' ' and field.state() == 'frozen':
                    color_fields.append(self._board[i][j])
                    
                    
            num_space = len(self._board[i]) - len(color_fields)      
                    
            
            for k in range(num_space):
                color_fields.insert(0, Field(' ', 'empty'))
            
            self._board[i] = color_fields
            
        self._handle_hide_field_gravity()
        
                    
    def _handle_hide_field_gravity(self) -> None:
        'Drop the hidden field of faller not shown on the board'
        if self._faller:
            faller = self._faller
            f_col = faller.col()
            f_row = faller.row()
            if f_row < 2:
                last_space_index = self._find_last_space_index(self._board[f_col])
                f_index = len(faller.fields()) - faller.num_space() - 1
                for b_row in range(last_space_index, -1, -1):
                    if f_index > -1:
                        self._board[f_col][b_row] = faller.fields()[f_index]
                        f_index -= 1
                        f_row += 1
                        self._faller.set_row(f_row)

               
    def _check_land(self, faller: Faller) -> bool:
        'Checks whether faller is landing, change state to landing if it is'
        f_col = faller.col()
        f_row = faller.row()
        if f_row == len(self._board[f_col])-1 or self._board[f_col][f_row + 1].attribute() != ' ':
            for field in faller.fields():
                field.set_state('landing')
            return True

        return False

    def _check_fall(self) -> bool:
        'Checks whether faller is in falling state'
        faller = self._faller
        fields = faller.fields()
        for field in fields:
            if field.state() != 'falling':
                return False

        return True

   
    def drop_faller(self) -> None:
        'Drop faller down by one field'
        faller = self._faller
        if self.has_faller():
            self._check_land(faller)
            if self._check_fall():
                f_col = faller.col()
                
                for row in range(len(self._board[f_col])):
                    if self._board[f_col][row].state() == 'falling':
                        self._board[f_col][row] = Field(' ', 'empty')
                
                faller.set_row(faller.row() + 1)
                next_c_row = faller.row()
                fields = faller.fields()
                for i in range(len(fields)):
                    b_row = next_c_row - i
                    if b_row > -1:
                        self._board[f_col][b_row] = fields[2 - i]

                self._check_land(faller)

    def freeze_faller(self) -> None:
        'Freezes the faller with landing state'
        for col in self._board:
            for row in col:
                if row.state() == 'landing':
                    row.set_state('frozen')
                    for field in self._faller.fields():
                        field.set_state('frozen')
               
            
                
    def move_faller_right(self, faller: Faller) -> None:
        '''
        Move faller to the direction given, move if the direction given is empty
        Else do nothing
        '''
        if faller:
            if faller.can_rotate():
                right_col = faller.col() + 1
                self._move_logic(faller, 'right', right_col)
        

    def move_faller_left(self, faller: Faller) -> None:
        '''
        Move faller to the direction given, move if the direction given is empty
        Else do nothing
        '''
        if faller:
            if faller.can_rotate():
                left_col = faller.col() - 1
                self._move_logic(faller, 'left', left_col)
                
                              
    def _move_logic(self, faller: Faller, direction: str, move_col: int) -> None:
        'Move logic shared by right and left faller move'
        
        field_present = []
        ori_row = []
        f_col = faller.col()
        f_row = faller.row()
        for row in range(len(self._board[0])):
            field = self._board[f_col][row]
            if field.state() == 'falling' or field.state() == 'landing':
                field_present.append(field)
                ori_row.append(row)
                
        if self._move_validity(ori_row, direction, move_col):
            for index, row in enumerate(ori_row):
                self._board[f_col][row] = Field(' ', 'empty')
                self._board[move_col][row] = field_present[index]
            faller.set_col(move_col)
            
            self._check_land(faller)
            if f_row != self._row - 1:
                if self._board[move_col][f_row+1].attribute() == ' ':
                    faller.set_state('falling')
            
                    
        

    def _move_validity(self, ori_row: list[int], direction: str, move_col: int) -> bool:
        'Return false if the moving direction is illegal, true otherwise'
        for row in ori_row: 
            if direction == 'left':
                if move_col == -1:
                    return False
            else:
                if move_col == len(self._board):
                    return False
            if self._board[move_col][row].attribute() != ' ':
                return False
        return True
    
    def check_end_game(self) -> None:
        '''
        If field is not fully display on the board when freezed and no
        match existed, ends the game and program.
        '''
        faller = self._faller
        if faller:
            if not self.has_faller() and faller.row() < 2 and \
            not faller.has_match() and not self.has_match():
                raise GameOver

    def handle_end_game(self) -> None:
        'Throws an exception to end the game'
        raise EndGame

def _check_int(num: int) -> None:
    'Checks for type of input given is int or not'
    if type(num) != int:
        raise NotIntError    
        
def _check_field(attribute: str, state: str) -> None:
    'Raise exception if attribute or state is invalid'
    if attribute != ' ':
        _check_color(attribute)
        _check_state(state)
    else:
        if state != 'empty':
            raise InvalidStateError
        
    
def _check_state(state: str) -> bool:
    '''
    Raises InvalidStateError is state of a color is invalid'
    Returns True if the state of the color is valid
    '''
    valid_state = ['frozen', 'landing', 'falling', 'matching']
    if state not in valid_state:
        raise InvalidStateError

    return True

        
def _check_color(colors: list[str] | str)  -> bool:
    '''
    Checks validity of colors,
    raises InvalidColorError if color is invalid
    Returns True if the color is valid
    '''
    valid_color = ['S','T','V','W','X','Y','Z']
    for color in colors:
        if not color in valid_color:
            raise InvalidColorError

    return True


def _check_size_validity(row: int, column: int) -> None:
    'Checks whether row or column is valid, raises an exception if not'
    if row < 4:
        raise InvalidRowError
    if column < 3:
        raise InvalidColumnError


def _check_faller_location(b_col: int, b_row: int, f_col: int, f_row: int) -> None:
    'Checks whether the faller is on the board, raise exception if it is not'
    if not (0 <= f_col < b_col and 0 <= f_row < b_row):
        raise InvalidFallerLocationError
        
                           
def _check_column_full(faller: Faller, board: list[list[Field]]) -> None:
    'Checks whether column is full for faller, raises an exception if it is'
    col = faller.col()
    field = board[col][0]
    if field.attribute() != ' ' and field.state() == 'frozen':
        raise ColumnFullError


def _check_content_validity(contents: list[str], row: int, column: int) -> None:
    '''
    Checks whether the content is valid in format, raises
    InvalidColorError is color letter is invalid, raises
    InvalidContentError if number of character does
    not equal number of column.
    '''
    if len(contents) != row:
        raise InvalidContentFormatError
    
    for content in contents:
        chars = list(content)
        if len(chars) != column:
            raise InvalidContentFormatError

