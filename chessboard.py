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

class Coord:
  def __init__(self, y: int=None, x: int=None, a_n: str=None):
    if (a_n is not None):
      self.y, self.x = NOTATION_TO_COORDS[a_n]
    else:      
      self.y = y
      self.x = x

  def __eq__(self, other):
    return self.y == other.y and self.x == other.x

  @staticmethod
  def is_in_bounds(y: int=None, x: int=None, a_n: str=None):
    if (a_n is not None):
      return a_n in NOTATION_TO_COORDS

    elif (y is not None and x is not None):
      return 0 <= y <= 7 and 0 <= x <= 7

    else:
      return False
    
class Move:
  def __init__(self, from_coord: Coord, to_coord):
    self.from_coord = from_coord
    self.to_coord = to_coord

  """
  The CPU player does not need this method.
  A move is invalid if:
  - It originates and/or ends at out of bounds coordinates.
  - It originates from a piece that the player does not own.
  - TODO: if the chess piece cannot make such a move.
  """
  @staticmethod
  def is_valid(board: 'Chessboard', color: str, from_coord: Coord, to_coord: Coord):
    if from_coord == to_coord:
      return False, "From and to should be different!"

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
          
          # An attacking white pawn
          if (abs(to_coord.x - from_coord.x) == 1
            and to_coord.y - from_coord.y == -1):
            return True, None

        # Non-attacking move
        else:         

          # A non-attacking white pawn in its starting position
          if (from_coord.y == 6                          
            and (to_coord.y == 5 or to_coord.y == 4)
            and to_coord.x == from_coord.x
            and board.empty_in(Coord(5, from_coord.x))):
            return True, None

          # A non-attacking white pawn not in its starting position
          if (from_coord.y != 6                          
            and (to_coord.y - from_coord.y == -1)
            and to_coord.x - from_coord.x == 0):
            return True, None

        return False, "Your pawn cannot move like that!"

      else: # color == 'b'
        # Attacking move
        if not board.empty_in(to_coord) and color != target_piece.color:        
          
          # An attacking black pawn
          if (abs(to_coord.x - from_coord.x) == 1
            and to_coord.y - from_coord.y == 1):
            return True, None     
        # Non-attacking move
        else:

          # A non-attacking black pawn in its starting position
          if (from_coord.y == 1                          
            and (to_coord.y == 2 or to_coord.y == 3)
            and to_coord.x == from_coord.x
            and board.empty_in(Coord(2, from_coord.x))):
            return True, None

          # A non-attacking black pawn not in its starting position
          if (from_coord.y != 1                          
            and (to_coord.y - from_coord.y == 1)
            and to_coord.x - from_coord.x == 0):
            return True, None

        return False, "Your pawn cannot move like that!"

    # A knight is a leaper, so we do not have to worry about it
    # 'jumping over' a few pieces in making a move.
    elif type(source_piece) == Knight:

      # Vertical L
      if (abs(to_coord.y - from_coord.y) == 2
        and abs(to_coord.x - from_coord.x) == 1):
        return True, None

      # Horizontal L
      if (abs(to_coord.y - from_coord.y) == 1
        and abs(to_coord.x - from_coord.x) == 2):
        return True, None
    
      return False, "Your knight cannot move like that!"

    # A bishop is a slider, so we must traverse the path between from_square
    # to to_square, checking if there is something blocking the way.
    elif type(source_piece) == Bishop:

      # If Bishop's movement is not a perfect diagonal: False
      if abs(to_coord.y - from_coord.y) != abs(to_coord.x - from_coord.x):
        return False, "Bishops can only move diagonally!"

      for y, x in zip(range(from_coord.y, to_coord.y, -1 if from_coord.y > to_coord.y else 1),
        range(from_coord.x, to_coord.x, -1 if from_coord.x > to_coord.x else 1)):
        if not board.empty_in(Coord(y, x)) and y != from_coord.y:
          return False, "Your bishop bumped into an impenetrable wall!"

      return True, None

    # A rook is a slider.  
    elif type(source_piece) == Rook:

      vert = abs(to_coord.y - from_coord.y)
      horz = abs(to_coord.x - from_coord.x)

      # If Rook's movement is not a straight line:
      if vert != 0 and horz != 0:
        return False, "Rooks can only move in one direction!"
      
      if vert:
        for y in range(from_coord.y, to_coord.y, -1 if from_coord.y > to_coord.y else 1):
          if not board.empty_in(Coord(y, from_coord.x)) and y != from_coord.y:
            return False, "Your Rook bumped into an impenetrable wall!"
      
      else: # horz  
        for x in range(from_coord.x, to_coord.x, -1 if from_coord.x > to_coord.x else 1):
          if not board.empty_in(Coord(from_coord.y, x)) and x != from_coord.x:
            return False, "Your Rook bumped into an impenetrable wall!"
      
      return True, None

    # A queen is a slider
    elif type(source_piece) == Queen:

      vert = abs(to_coord.y - from_coord.y)
      horz = abs(to_coord.x - from_coord.x)
      
      # If Queen's movement is not a straight line:
      if vert != 0 and horz != 0 and vert != horz:
        return False, "Your Queen can only move in a straight line!"
      
      if vert == 0:
        for x in range(from_coord.x, to_coord.x, -1 if from_coord.x > to_coord.x else 1):
          if not board.empty_in(Coord(from_coord.y, x)) and x != from_coord.x:
            return False, "Your Queen bumped into an impenetrable wall!"
      
      elif horz == 0:
        for y in range(from_coord.y, to_coord.y, -1 if from_coord.y > to_coord.x else 1):
          if not board.empty_in(Coord(y, from_coord.x)) and y != from_coord.y:
            return False, "Your Queen bumped into an impenetrable wall!"
      
      # Perfect diagonal
      else:
        for y, x in zip(range(from_coord.y, to_coord.y, -1 if from_coord.y > to_coord.y else 1), 
          range(from_coord.x, to_coord.x, -1 if from_coord.x > to_coord.x else 1)):
          if not board.empty_in(Coord(y, x)) and y != from_coord.y:
            return False, "Your Queen bumped into an impenetrable wall!"

      return True, None

    # type(source_piece) == King
    # A King can only move one tile, so no path checking needed.
    else: 

      if abs(to_coord.y - from_coord.y) > 1:
        return False, "Your King can only move 1 tile per turn!"
      
      if abs(to_coord.x - from_coord.x) > 1:
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

  def piece_in(self, coord: Coord):
    return self.board[coord.y][coord.x]

  def empty_in(self, coord: Coord):
    return type(self.board[coord.y][coord.x]) == Empty

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
          if Coord(y, x) == last_move.from_coord:
            res += f"{Ccolor.OKBLUE}{self.board[y][x]}{Ccolor.ENDC} "
          elif Coord(y, x) == last_move.to_coord:
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
      king = self.piece_in(king_coords)

      for valid_move in king.valid_moves((king_coords)):
        position = self.make_move(valid_move)

        if not position.is_check():
          res.append(position)

    # Non-double check
    else:
      for y in range(8):
        for x in range(8):
          piece = self.piece_in(Coord(y, x))
          if type(piece) == Empty: continue
          if piece.color != color: continue

          for valid_move in piece.valid_moves(self, Coord(y, x)):
            position = self.make_move(valid_move)
            
            if not position.is_check():
              res.append(position)

    return res
          

  """
  Called to verify if the last move was legal or not.

  Last move was legal if it does not place P King under a check.
  """
  # def is_check(self, color):
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
  # def is_double_check(self, last_move):

  def evaluate(self):
    aggregate_value = 0
    
    # Static piece value evaluations
    for piece_type, quantity in self.inventory['w'].items():
      aggregate_value += PIECE_VALUE[piece_type]

    for piece_type, quantity in self.inventory['b'].items():
      aggregate_value -= PIECE_VALUE[piece_type]

    # Bishop pair bonus
    if self.inventory['w'][Bishop] == 2:
      aggregate_value += PIECE_VALUE['BISHOP_PAIR_BONUS']

    if self.inventory['b'][Bishop] == 2:
      aggregate_value -= PIECE_VALUE['BISHOP_PAIR_BONUS']

    # Positional value evaluations
    for y in range(8):
      for x in range(8): 
        if (self.empty_in(Coord(y,x))):
          continue
        
        piece = self.piece_in(Coord(y, x))

        # White maximizes
        if (piece.color == 'w'):
          aggregate_value += PIECE_SQUARE_TABLES[type(piece)][y][x]

        # Black minimizes
        else:
          # abs(y - 7) to 'vertical flip' PST.
          # If Black's pawn is in (4, 3) for example, we should index into
          # PST[Pawn][3][3] == 15, not PST[Pawn][4][3] == 10.
          aggregate_value -= PIECE_SQUARE_TABLES[type(piece)][abs(y - 7)][x]

    return aggregate_value
      
  def make_move(self, move: Move):
    new_position = copy.deepcopy(self)
    new_position.last_move = move

    # No attack
    if new_position.empty_in(move.to_coord):
      new_position.board[move.from_coord.y][move.from_coord.x], \
      new_position.board[move.to_coord.y][move.to_coord.x] =    \
      new_position.board[move.to_coord.y][move.to_coord.x],     \
      new_position.board[move.from_coord.y][move.from_coord.x]
    
    # Attack move
    else:
      self.inventory[new_position.piece_in(move.to_coord).color][type(new_position.piece_in(move.to_coord))] -= 1
      new_position.board[move.to_coord.y][move.to_coord.x] = \
      new_position.board[move.from_coord.y][move.from_coord.x]
      new_position.board[move.from_coord.y][move.from_coord.x] = Empty()

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