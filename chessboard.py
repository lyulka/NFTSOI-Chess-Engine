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

class Chessboard:
  transpositions = {}

  def __init__(self, last_move: Move=None):
    self.board = INITIAL_BOARD
    self.inventory = INITIAL_INVENTORY
    self.w_king_coords = (7, 3)
    self.b_king_coords = (0, 4)
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
    
    if (last_move is None): 
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