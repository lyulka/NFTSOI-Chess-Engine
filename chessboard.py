from pieces import *
import copy

class Ccolor:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

INDEX_TO_LETTER = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

NOTATION_TO_COORDS = {
  'a8': (0, 0), 'b8': (0, 1), 'c8': (0, 2), 'd8': (0, 3), 'e8': (0, 4), 'f8': (0, 5), 'g8': (0, 6), 'h1': (0, 7),
  'a7': (1, 0), 'b7': (1, 1), 'c7': (1, 2), 'd7': (1, 3), 'e7': (1, 4), 'f7': (1, 5), 'g7': (1, 6), 'h7': (1, 7),
  'a6': (2, 0), 'b6': (2, 1), 'c6': (2, 2), 'd6': (2, 3), 'e6': (2, 4), 'f6': (2, 5), 'g6': (2, 6), 'h6': (2, 7),
  'a5': (3, 0), 'b5': (3, 1), 'c5': (3, 2), 'd5': (3, 3), 'e5': (3, 4), 'f5': (3, 5), 'g5': (3, 6), 'h5': (3, 7),
  'a4': (4, 0), 'b4': (4, 1), 'c4': (4, 2), 'd4': (4, 3), 'e4': (4, 4), 'f4': (4, 5), 'g4': (4, 6), 'h4': (4, 7),
  'a3': (5, 0), 'b3': (5, 1), 'c3': (5, 2), 'd3': (5, 3), 'e3': (5, 4), 'f3': (5, 5), 'g3': (5, 6), 'h3': (5, 7),
  'a2': (6, 0), 'b2': (6, 1), 'c2': (6, 2), 'd2': (6, 3), 'e2': (6, 4), 'f2': (6, 5), 'g2': (6, 6), 'h2': (6, 7),
  'a1': (7, 0), 'b1': (7, 1), 'c1': (7, 2), 'd1': (7, 3), 'e1': (7, 4), 'f1': (7, 5), 'g1': (7, 6), 'h1': (7, 7),
}

INITIAL_BOARD = [
  [Rook('b'),   Knight('b'), Bishop('b'), Queen('b'),  King('b'),   Bishop('b'), Knight('b'), Rook('b')],
  [Pawn('b'),   Pawn('b'),   Pawn('b'),   Pawn('b'),   Pawn('b'),   Pawn('b'),   Pawn('b'),   Pawn('b')],
  [Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty()  ],
  [Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty()  ],
  [Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty()  ],
  [Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty(),     Empty()  ],
  [Pawn('w'),   Pawn('w'),   Pawn('w'),   Pawn('w'),   Pawn('w'),   Pawn('w'),   Pawn('w'),   Pawn('w')],
  [Rook('w'),   Knight('w'), Bishop('w'), King('w'),   Queen('w'),  Bishop('w'), Knight('w'), Rook('w')],
]

INITIAL_INVENTORY = {
  'b': {
    Pawn: 8,
    Knight: 2,
    Bishop: 2,
    Rook: 2,
    Queen: 1,
    King: 1,
  },
  'w': {
    Pawn: 8,
    Knight: 2,
    Bishop: 2,
    Rook: 2,
    Queen: 1,
    King: 1,
  }
}

# Based on GM Larry Kaufman's analysis:
# Available at: https://www.danheisman.com/evaluation-of-material-imbalances.html
PIECE_VALUE = {
  Pawn: 100,
  Knight: 325,
  Bishop: 325,
  Rook: 500,
  Queen: 975,
  'BISHOP_PAIR_BONUS': 0.5, 
}

# Based on: https://github.com/emdio/secondchess/blob/master/secondchess.c
# We will 'vertically flip' this by means of a trick with abs() later on.
PIECE_SQUARE_TABLES = {
  Pawn: [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 15, 15, 0, 0, 0],
    [0, 0, 0, 10, 10, 0, 0, 0],
    [0, 0, 0, 5, 5, 0, 0, 0],
    [0, 0, 0, -25, -25, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
  ],
  Knight: [
    [-40, -25, -25, -25, -25, -25, -25, -40],
    [-30, 0, 0, 0, 0, 0, 0, -30],
    [-30, 0, 0, 0, 0, 0, 0, -30],
    [-30, 0, 0, 15, 15, 0, 0, -30],
    [-30, 0, 0, 15, 15, 0, 0, -30],
    [-30, 0, 10, 0, 0, 10, 0, -30],
    [-30, 0, 0, 5, 5, 0, 0, -30],
    [-40, -30, -25, -25, -25, -25, -30, -40],
  ],
  Bishop: [
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 0, 5, 0, 0, 5, 0, -10],
    [-10, 0, 0, 10, 10, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 0, 5, 0, 0, 5, 0, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, -20, -20, -20, -20, -20, -20, -10],
  ],
  Rook: [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [10, 10, 10, 10, 10, 10, 10, 10],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 5, 0, 0, 0],
  ],
  King: [
    [-25, -25, -25, -25, -25, -25, -25, -25],
    [-25, -25, -25, -25, -25, -25, -25, -25],
    [-25, -25, -25, -25, -25, -25, -25, -25],
    [-25, -25, -25, -25, -25, -25, -25, -25],
    [-25, -25, -25, -25, -25, -25, -25, -25],
    [-25, -25, -25, -25, -25, -25, -25, -25],
    [-25, -25, -25, -25, -25, -25, -25, -25],
    [10, 15, -15, -15, -15, -15, 15, 10],
  ],
}

class Move:
  def __init__(self, from_square: str, to_square: str):
    self.from_coord = NOTATION_TO_COORDS[from_square]
    self.to_coord = NOTATION_TO_COORDS[to_square]

  """
  The CPU player does not need this method.
  A move is invalid if:
  - It originates and/or ends at out of bounds coordinates.
  - It originates from a piece that the player does not own.
  - TODO: if the chess piece cannot make such a move.
  """
  @staticmethod
  def is_valid(board: 'Chessboard', color: str, from_square: str, to_square: str):
    from_coord = NOTATION_TO_COORDS.get(from_square, False)
    to_coord = NOTATION_TO_COORDS.get(to_square, False)

    # Why?
    if from_square == to_square:
      return False, "You cannot not move a piece!"

    # Out of bounds
    if (not from_coord or not to_coord):
      return False, "You're going out of bounds!"

    source_piece = board.piece_in(from_coord)
    target_piece = board.piece_in(to_coord)

    # If source is empty or player does not own piece in source: False
    if (board.empty_in(from_coord)
      or source_piece.color != color):
      return False, "You don't have a piece on the source square!"

    # If target piece is not empty and player's own piece is in target: False
    if not board.empty_in(to_coord) and target_piece.color == color:
      return False, "A piece you own is on the target square!"
    
    if type(source_piece) == Pawn:
      if color == 'w':
        # Attacking move
        if not board.empty_in(to_coord) and color != target_piece.color:
          # An attacking white pawn can move horizontally by 1 square
          # And move vertically in the negative vertical direction by 1 square
          if (abs(to_coord[1] - from_coord[1]) == 1
            and to_coord[0] - from_coord[0] == -1):
            return True, None
        # Non-attacking move
        else:                                              
          # A non-attacking white pawn in its starting position
          # can move 1 or 2 squares forward
          # but cannot move horizontally
          # And it cannot jump over an occupied spot.
          if (from_coord[0] == 6                          
            and (to_coord[0] == 5 or to_coord[0] == 4)
            and to_coord[1] - from_coord[1] == 0
            and board.empty_in(to_coord)):
            return True, None
          # A non-attacking white pawn not in its starting position
          # can move exactly 1 square forward
          # but cannot move horizontally
          if (from_coord[0] != 6                          
            and (to_coord[0] - from_coord[0] == -1)
            and to_coord[1] - from_coord[1] == 0):
            return True, None

        return False, "Your pawn cannot move like that!"

      else: # color == 'b'
        # Attacking move
        if not board.empty_in(to_coord) and color != target_piece.color:        
          # An attacking white pawn can move horizontally by 1 square
          # And move vertically in the positive vertical direction by 1 square
          if (abs(to_coord[1] - from_coord[1]) == 1
            and to_coord[0] - from_coord[0] == 1):
            return True, None     
        # Non-attacking move
        else:
          # A non-attacking white pawn in its starting position
          # can move 1 or 2 squares forward
          # but cannot move horizontally
          if (from_coord[0] == 1                          
            and (to_coord[0] == 2 or to_coord[0] == 3)
            and to_coord[1] - from_coord[1] == 0):
            return True, None
          # A non-attacking white pawn not in its starting position
          # can move exactly 1 square forward
          # but cannot move horizontally
          if (from_coord[0] != 1                          
            and (to_coord[0] - from_coord[0] == 1)
            and to_coord[1] - from_coord[1] == 0):
            return True, None

        return False, "Your pawn cannot move like that!"

    # A knight is a leaper, so we do not have to worry about it
    # 'jumping over' a few pieces in making a move.
    elif type(source_piece) == Knight:

      # Vertical L
      if (abs(to_coord[0] - from_coord[0]) == 2
        and abs(to_coord[1] - from_coord[1]) == 1):
        return True, None
      # Horizontal L
      if (abs(to_coord[0] - from_coord[0]) == 1
        and abs(to_coord[1] - from_coord[1]) == 2):
        return True, None
    
      return False, "Your knight cannot move like that!"

    # A bishop is a slider, so we must traverse the path between from_square
    # to to_swaure, checking if there is something blocking the way.
    elif type(source_piece) == Bishop:

      # If Bishop's movement is not a perfect diagonal: False
      if abs(to_coord[0] - from_coord[0]) - abs(to_coord[1] - from_coord[1]) != 0:
        return False, "Bishops can only move diagonally!"

      for y, x in zip(range(from_coord[0], to_coord[0]), range(from_coord[1]), to_coord[1]):
        if not board.empty_in((y, x)) and y != from_coord[0]:
          return False, "Your bishop bumped into an impenetrable wall!"

      return True, None

    # A rook is a slider.  
    elif type(source_piece) == Rook:

      vert = abs(to_coord[0] - from_coord[0])
      horz = abs(to_coord[1] - from_coord[1])
      # If Rook's movement is not a straight line:
      if vert != 0 and horz != 0:
        return False, "Rooks can only move in one direction!"
      if vert:
        for y in range(from_coord[0], to_coord[0]):
          if not board.empty_in((y, from_coord[1])) and y != from_coord[0]:
            return False, "Your Rook bumped into an impenetrable wall!"
      else: # horz  
        for x in range(from_coord[1], to_coord[1]):
          if not board.empty_in((from_coord[0], x)) and x != from_coord[1]:
            return False, "Your Rook bumped into an impenetrable wall!"
      
      return True, None

    # A queen is a slider
    elif type(source_piece) == Queen:

      vert = abs(to_coord[0] - from_coord[0])
      horz = abs(to_coord[1] - from_coord[1])
      # If Queen's movement is not a straight line:
      if vert != 0 and horz != 0 and vert != horz:
        return False, "Your Queen can only move in a straight line!"
      if vert == 0:
        for x in range(from_coord[1], to_coord[1]):
          if not board.empty_in((from_coord[0], x)) and x != from_coord[1]:
            return False, "Your Queen bumped into an impenetrable wall!"
      elif horz == 0:
        for y in range(from_coord[0], to_coord[0]):
          if not board.empty_in((y, from_coord[1])) and y != from_coord[0]:
            return False, "Your Queen bumped into an impenetrable wall!"
      # Perfect diagonal
      else:
        for y, x in zip(range(from_coord[0], to_coord[0]), range(from_coord[1]), to_coord[1]):
          if not board.empty_in((y, x)) and y != from_coord[0]:
            return False, "Your Queen bumped into an impenetrable wall!"

      return True, None

    # type(source_piece) == King
    # A King can only move one tile, so no path checking needed.
    else: 

      if abs(to_coord[0] - from_coord[0]) > 1:
        return False, "Your King can only move 1 tile per turn!"
      if abs(to_coord[1] - from_coord[1]) > 1:
        return False, "Your King can only move 1 tile per turn!"

      return True, None
        
    return True, None

class Chessboard:
  transpositions = {}

  def __init__(self, w_king_coords: tuple=(7,3), b_king_coords: tuple=(0, 4), last_move: Move=None):
    self.board = INITIAL_BOARD
    self.inventory = INITIAL_INVENTORY
    self.w_king_coords = w_king_coords
    self.b_king_coords = b_king_coords
    self.last_move = None

  def piece_in(self, coord: tuple):
    return self.board[coord[0]][coord[1]]

  def empty_in(self, coord: tuple):
    return type(self.board[coord[0]][coord[1]]) == Empty

  """
  By default, black is rendered on top, white on bottom.
  Toggle vertical_flip to reverse this.
  """
  def print_board(self, last_move: Move, vertical_flip: bool=False):
    res = ""

    start, end, step = 0, 8, 1
    if (vertical_flip):
      start, end, step = 7, -1, -1
    
    if (last_move == None): 
      for y in range(start, end, step):
        for x in range(start, end, step):
            res += f"{self.board[y][x]} "
        res += f" {8 - y}\n"
    
    else:
      for y in range(start, end, step):
        for x in range(start, end, step):
          if (y, x) == last_move.from_coord:
            res += f"{Ccolor.OKBLUE}{self.board[y][x]}{Ccolor.ENDC} "
          elif (y, x) == last_move.to_coord:
            res += f"{Ccolor.WARNING}{self.board[y][x]}{Ccolor.ENDC} "
          else:
            res += f"{self.board[y][x]} "
        res += f" {8 - y}\n"

    for i in range(start, end, step):
      res += f"{INDEX_TO_LETTER[i]} "
    res += "\n"
        
    print(res)

  """
  TODO: Legal successor positions generator.

  The flow of a single game tree node expansion looks like this:
  - is_double_check?
  - generate pseudolegal moves & positions.
  - is_check?
  - Yes -> make_move
  - recurse.
  """
  def legal_positions(self, color: str):
    res = [] # Resultant Chessboard[]

    # Double check using last_move
    if (self.is_double_check()):
      king_coords = self.w_king_coords if color == 'w' else self.b_king_coords
      king = self.get_piece(king_coords)

      for valid_move in king.valid_moves((king_coords)):
        position = self.make_move(valid_move)

        if not position.is_check():
          res.append(position)

    # Non-double check
    else:
      for y in range(8):
        for x in range(8):
          piece = self.get_piece((y, x))
          if type(piece) == Empty: continue
          if piece.color != color: continue

          for valid_move in piece.valid_moves((y, x)):
            position = self.make_move(valid_move)
            
            if not position.is_check():
              res.append(position)

    return res
          

  """
  Called to verify if the last move was legal or not.

  Last move was legal if it does not place P King under a check.
  """
  def is_check(self, color):
    # Replace P King with P Pawn. Generate all moves for P Pawn.
    # If move causes Pawn to take: E Queen or E Bishop or E Pawn, return False.

    # Not threatened by pawn.

    # Replace P King with P Knight. Generate all moves for P Knight.
    # If move causes Knight to take: E Knight, return False.

    # Not threatened by knight.

    # Replace P King with P Bishop: Generate all moves for P Bishop.
    # If move causes Bishop to take: E Queen or E Bishop, return False.

    # Not threatened by bishop.

    # Replace P King with P Rook: Generate all moves for P Rook.
    # If move causes Rook to take: E Queen or E Rook, return False.

    # Not threatened by rook or queen.

    # Replace P King: Generate all moves for P King.
    # If more causes King to take: E King, return False.

    # Not threatened by king.


  """
  Called before the searches further down the game tree.

  While is_check considers whether the current player's last move puts
  their King in check, is_double_check whether the enemy player's last
  move puts the current player in check.
  """
  def is_double_check(self, last_move):

  def evaluate(self):
    
    
  def make_move(self, move: Move):
    new_position = copy.deepcopy(self)
    new_position.last_move = move

    # No attack
    if new_position.empty_in(move.to_coord):
      new_position.board[move.from_coord[0]][move.from_coord[1]], \
      new_position.board[move.to_coord[0]][move.to_coord[1]] =    \
      new_position.board[move.to_coord[0]][move.to_coord[1]],     \
      new_position.board[move.from_coord[0]][move.from_coord[1]]
    
    # Attack move
    else:
      self.inventory[type(new_position.piece_in(move.to_coord))] -= 1
      new_position.board[move.to_coord[0]][move.to_coord[1]] = \
      new_position.board[move.from_coord[0]][move.from_coord[1]]
      new_position.board[move.from_coord[0]][move.from_coord[1]] = Empty()

    # If either King is moved, update his position.
    moved = new_position.piece_in(move.to_coord)

    if (type(moved) == King):
      if (moved.color == 'b'):
        self.b_king_coords = move.to_coord
      else: # moved.color == 'w'
        self.w_king_coords = move.to_coord

    return new_position

  """
  TODO: Decide whether game has ended.
  """
  def get_victor(self):
    return False