import pygame
import columns_logic
import random

_FRAME_RATE = 1
_BACKGROUND_COLOR = pygame.Color(0, 0, 0)
_INITIAL_WIDTH = 750
_INITIAL_HEIGHT = 700
_ROW = 13
_COLUMN = 6

_FRAC_BOARD_TOP_LEFT_X = 6/18
_FRAC_BOARD_TOP_LEFT_Y = 1/15
_FRAC_BOARD_BOTTOM_Y = 14/15
_FRAC_BOARD_RIGHT_X = 12/18
_FRAC_BOARD_WIDTH = 6/18
_FRAC_BOARD_HEIGHT = 13/15

_BLACK = pygame.Color(0, 0, 0)
_WHITE = pygame.Color(255, 255, 255)
_RED = pygame.Color(237, 12, 12)
_BROWN = pygame.Color(89, 61, 19)
#Seven display color
_ORANGE = pygame.Color(237, 128, 12)
_YELLOW = pygame.Color(237, 237, 12)
_GREEN = pygame.Color(16, 237, 12)
_CYAN = pygame.Color(12, 237, 222)
_BLUE = pygame.Color(12, 128, 237)
_PURPLE = pygame.Color(124, 12, 237)
_PINK = pygame.Color(237, 12, 226)
_COLORS = [_ORANGE, _YELLOW, _GREEN, _CYAN, _BLUE, _PURPLE, _PINK]
_COLOR_DICT = {'S': _ORANGE, 'T': _YELLOW, 'V': _GREEN, 'W': _CYAN, 'X': _BLUE, 'Y': _PURPLE, 'Z': _PINK}

            
class ColumnsGame:
    def __init__(self):
        self._cs = columns_logic.ColumnsState(_ROW, _COLUMN)
        self._running = True
        
    def run(self) -> None:
        pygame.init()
        try:
            clock = pygame.time.Clock()
            self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))
            self._update_pix_values()
            self._draw_background()
            
            while self._running:
                clock.tick(_FRAME_RATE)
                self._create_faller()
                self._handle_events()
                self._draw_fields()
                self._handle_time_pass()
                self._draw_frame()
                
        except columns_logic.EndGame:
            self._game_over()
        except columns_logic.ColumnFullError:
            self._game_over()
        except columns_logic.GameOver:
            self._game_over()       
        finally:
            pygame.quit()

    def _create_surface(self, size: tuple[int, int]) -> None:
        'Establish self variable surface'
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)

    def _update_pix_values(self) -> None:
        'Update the pix value when window resized'
        self._surface = pygame.display.get_surface()
        width = self._surface.get_width()
        height = self._surface.get_height()
        
        self._pix_board_width = self._frac_to_pix(_FRAC_BOARD_WIDTH, width)
        self._pix_board_height = self._frac_to_pix(_FRAC_BOARD_HEIGHT, height)
        self._pix_grid_width = self._pix_board_width / 6
        self._pix_grid_height = self._pix_board_height / 13
        
        self._pix_board_top_left_x = self._frac_to_pix(_FRAC_BOARD_TOP_LEFT_X, width)
        self._pix_board_top_left_y = self._frac_to_pix(_FRAC_BOARD_TOP_LEFT_Y, height)
        self._pix_board_right_x = self._frac_to_pix(_FRAC_BOARD_RIGHT_X, width)
        self._pix_board_bottom_y = self._frac_to_pix(_FRAC_BOARD_BOTTOM_Y, height)

    def _draw_background(self) -> None:
        'Fill background color and draw the grid board'
        self._surface.fill(_BACKGROUND_COLOR)
        
        self._draw_board()
        
        self._draw_grid_line()

    def _draw_board(self) -> None:
        'Draw the rectangle board'
        rect = self._create_rect_board()
        pygame.draw.rect(self._surface, _WHITE, rect)

    def _create_rect_board(self) -> pygame.Rect:
        'Create a rectangle object and returns it'
        return pygame.Rect(self._pix_board_top_left_x, self._pix_board_top_left_y, self._pix_board_width, self._pix_board_height)

    def _draw_grid_line(self) -> None:
        'Draws the grid line on the board'
        for i in range(_COLUMN):
            pix_grid_x = self._pix_board_top_left_x + int(i * self._pix_grid_width)
            pygame.draw.line(self._surface, _BLACK, (pix_grid_x, self._pix_board_top_left_y), (pix_grid_x, self._pix_board_bottom_y))

        for j in range(_ROW):
            pix_grid_y = self._pix_board_top_left_y + int(j * self._pix_grid_height)
            pygame.draw.line(self._surface, _BLACK, (self._pix_board_top_left_x, pix_grid_y), (self._pix_board_right_x, pix_grid_y))

            
    def _create_faller(self) -> None:
        '''
        Create and display the a faller with random color at random column
        If some columns are full only create at empty column available.
        '''
        if not self._cs.has_faller() and not self._cs.has_match():
            valid_col = self._get_valid_col()
            c1 = self._create_random_field()
            c2 = self._create_random_field()
            c3 = self._create_random_field()
            if valid_col:
                self._faller = columns_logic.Faller(random.choice(valid_col), c1, c2, c3)
            else:
                self._faller = columns_logic.Faller(random.randint(0, _COLUMN - 1), c1, c2, c3)
            self._cs.create_faller(self._faller)

    def _get_valid_col(self) -> list[int]:
        'Get the empty col that a faller and appear on'
        valid_col = []
        board = self._cs.board()
        for c in range(len(board)):
            if board[c][0].attribute() == ' ':
                valid_col.append(c)

        return valid_col
    
    def _create_random_field(self) -> columns_logic.Field:
        'Creates a field with random color'
        rand_c = random.choice(_COLORS)
        letter_c = ''
        for key, value in _COLOR_DICT.items():
            if rand_c == value:
                letter_c = key
                
        return columns_logic.Field(letter_c, 'falling')

    def _handle_events(self) -> None:
        'Handle all the events here'
        for event in pygame.event.get():
            self._handle_event(event)


    def _handle_event(self, event) -> None:
        'Handle single event'
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.VIDEORESIZE:
            self._resize_surface(event.size)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._move_left()
            elif event.key == pygame.K_RIGHT:
                self._move_right()
            elif event.key == pygame.K_SPACE:
                self._rotate()

            


    def _move_left(self) -> None:
        'Moves the faller to the left'
        self._cs.move_faller_left(self._faller)

    def _move_right(self) -> None:
        'Moves the faller to the right'
        self._cs.move_faller_right(self._faller)

    def _rotate(self) -> None:
        'Rotates the faller'
        self._cs.rotate_faller(self._faller)

        
    def _handle_time_pass(self) -> None:
        'Handles the time pass and update the board'
        if self._cs.has_faller():
            self._cs.freeze_faller()
            self._cs.find_match()   
            self._cs.drop_faller()
        else:
            self._cs.remove_match()
            self._cs.apply_gravity()
            self._cs.find_match()
        
        
        self._cs.check_end_game()
        
    def _draw_fields(self) -> None:
        'Draw all the fields present on the board'
        board = self._cs.board()
        for c in range(_COLUMN):
            for r in range(_ROW):
                attribute = board[c][r].attribute()
                state = board[c][r].state()
                rect = self._create_rect_field(c, r)
                if attribute != ' ':
                    color = _COLOR_DICT[attribute]
                    self._draw_field(rect, color)
                else:
                    self._clear_field(rect)
                if state == 'matching':
                    self._signal_matching(rect)
                elif state == 'landing':
                    self._signal_landing(rect)

    
    def _create_rect_field(self, col: int, row: int) -> pygame.Rect:
        'Creates a rectangle using column and row given'
        pix_tl_x = self._pix_board_top_left_x + int(col * self._pix_grid_width) + 1 
        pix_tl_y = self._pix_board_top_left_y + int(row * self._pix_grid_height) + 1
        rect = pygame.Rect(pix_tl_x, pix_tl_y, self._pix_grid_width - 1 , self._pix_grid_height - 1)

        return rect

    def _draw_field(self, rect: pygame.Rect, color: pygame.Color) -> None:
        'Draw the field on corresponding board position'
        pygame.draw.rect(self._surface, color, rect)

    def _clear_field(self, rect: pygame.Rect) -> None:
        'Clear the field that does not have any color'
        tl_x = rect.x
        tl_y = rect.y
        tl_x += 1
        tl_y += 1
        color = self._surface.get_at((tl_x, tl_y))
        if color != _WHITE:
            pygame.draw.rect(self._surface, _WHITE, rect)

    def _signal_landing(self, rect: pygame.Rect) -> None:
        'Singal the landing by color brown'
        pygame.draw.rect(self._surface, _BROWN, rect, 5)


    def _signal_matching(self, rect: pygame.Rect) -> None:
        'Singal the matching by color red'
        pygame.draw.rect(self._surface, _RED, rect, 5)

        
    def _frac_to_pix(self, frac: float, max_pix: int) -> int:
        'Convert fractional value into pixel value'
        return int(frac * max_pix)
        
    
    def _stop_running(self) -> None:
        'Ends the program'
        self._running = False

    def _resize_surface(self, size: tuple[int, int]) -> None:
        'Update the surface to whatever size user change to'
        pygame.display.set_mode(size, pygame.RESIZABLE)
        self._update_pix_values()
        self._draw_background()

    
    def _draw_frame(self) -> None:
        'Update the board'
        pygame.display.flip()

    def _game_over(self) -> None:
        'Freeze the game board to represent game over'
        self._stop_running()
        game_over = True
        self._draw_fields()
        self._draw_frame()
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                elif event.type == pygame.VIDEORESIZE:
                    self._resize_surface(event.size)
                    self._draw_fields()
                    self._draw_frame()
        
    


if __name__ == '__main__':
    ColumnsGame().run()
