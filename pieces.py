from move import Move
from coord import Coord

class Empty:
  def __str__(self):
    return u'\u25c7'

class Piece:
  def __init__(self, color):
    self.color = color

  def is_enemy(self, other: 'Piece'):
    if type(other) == Empty:
      return False

    return self.color != other.color

  def is_friend(self, other: 'Piece'):
    if type(other) == Empty:
      return False

    return self.color == other.color

class Pawn(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2659'
    return u'\u265f'

  # Valid move generation is used strictly to generate moves
  # for the AI player. The validity of moves inputted by the
  # human player is checked in Move.is_valid.
  def valid_moves(self, board: 'Chessboard', from_c: 'Coord'):
    moves = []

    if self.color == 'w':

      # Pawn is in starting position
      if (from_c.y == 6 and board.empty_in(Coord(5, from_c.x))
        and board.empty_in(Coord(4, from_c.x))):
        moves.append(Move(from_c, Coord(4, from_c.x))) # Move forward 2 steps

      if board.empty_in(Coord(from_c.y - 1, from_c.x)):
        moves.append(Move(from_c, Coord(from_c.y - 1, from_c.x))) # Move forward 1 step

      # Attacking north-west
      t_y, t_x = from_c.y - 1, from_c.x - 1
      if (Coord.is_in_bounds(t_y, t_x)
        and self.is_enemy(board.piece_in(Coord(t_y, t_x)))):
        moves.append(Move(from_c, Coord(t_y, t_x)))
      
      # Attacking north-east
      t_y, t_x = from_c.y - 1, from_c.x + 1
      if (Coord.is_in_bounds(t_y, t_x)
        and self.is_enemy(board.piece_in(Coord(t_y, t_x)))):
        moves.append(Move(from_c, Coord(t_y, t_x)))

    else: # self.color == 'b'

      if (from_c.y == 1 and board.empty_in(Coord(2, from_c.x))
        and board.empty_in(Coord(3, from_c.x))):
        moves.append(Move(from_c, Coord(3, from_c.x)))

      if board.empty_in(Coord(from_c.y + 1, from_c.x)):
        moves.append(Move(from_c, Coord(from_c.y + 1, from_c.x)))

      # Attacking south-west
      t_y, t_x = from_c.y + 1, from_c.x - 1
      if (Coord.is_in_bounds(t_y, t_x)
        and self.is_enemy(board.piece_in(Coord(t_y, t_x)))):
        moves.append(Move(from_c, Coord(t_y, t_x)))
      
      # Attacking south-east
      t_y, t_x = from_c.y + 1, from_c.x + 1
      if (Coord.is_in_bounds(t_y, t_x)
        and self.is_enemy(board.piece_in(Coord(t_y, t_x)))):
        moves.append(Move(from_c, Coord(t_y, t_x)))

    return moves 


class Knight(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2658'
    return u'\u265e'

  def valid_moves(self, board: 'Chessboard', from_c: 'Coord'):
    moves = []

    # Enumerating possible moves clockwise, starting from North
    possible_targets = (
      (from_c.y - 2, from_c.x + 1),
      (from_c.y - 1, from_c.x + 2),
      (from_c.y + 1, from_c.x + 2),
      (from_c.y + 2, from_c.x + 1),
      (from_c.y + 2, from_c.x - 1),
      (from_c.y + 1, from_c.x - 2),
      (from_c.y - 1, from_c.x - 2),
      (from_c.y - 2, from_c.x - 1),
    )

    for t_y, t_x in possible_targets:
      if (Coord.is_in_bounds(t_y, t_x)
        and (board.empty_in(Coord(t_y, t_x)) or board.piece_in(Coord(t_y, t_x)).is_enemy(self))):
        moves.append(Move(from_c, Coord(t_y, t_x)))

    return moves

class Bishop(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2657'
    return u'\u265d'

  def valid_moves(self, board: 'Chessboard', from_c: 'Coord'):
    moves = []

    offsets = (
      (-1, 1), # Move north-east
      (1, 1), # Move south-east
      (1, -1), # Move south-west
      (-1, -1), # Move north-west
    )

    for offset in offsets:
      t_y, t_x = from_c.y, from_c.x

      while True:
        t_y, t_x = t_y + offset[0], t_x + offset[1]
        
        # Exceeded bounds
        if not Coord.is_in_bounds(t_y, t_x):
          break
        
        t_c = Coord(t_y, t_x)
        move = Move(from_c, t_c)

        # Nobody here
        if board.empty_in(t_c):
          moves.append(move)
          continue

        # Bump into enemy
        if board.piece_in(t_c).is_enemy(self):
          moves.append(move)
          break
        
        # Bump into friend
        if board.piece_in(t_c).is_friend(self):
          break

    return moves

class Rook(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2656'
    return u'\u265c'

  def valid_moves(self, board: 'Chessboard', from_c: 'Coord'):
    moves = []

    offsets = (
      (-1, 0), # Move north
      (0, 1), # Move east
      (1, 0), # Move south
      (0, -1), # Move west
    )

    for offset in offsets:
      t_y, t_x = from_c.y, from_c.x

      while True:
        t_y, t_x = t_y + offset[0], t_x + offset[1]
        
        # Exceeded bounds
        if not Coord.is_in_bounds(t_y, t_x):
          break
        
        t_c = Coord(t_y, t_x)
        move = Move(from_c, t_c)

        # Nobody here
        if board.empty_in(t_c):
          moves.append(move)
          continue

        # Bump into enemy
        if board.piece_in(t_c).is_enemy(self):
          moves.append(move)
          break
        
        # Bump into friend
        if board.piece_in(t_c).is_friend(self):
          break

    return moves

class Queen(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2655'
    return u'\u265b'

  def valid_moves(self, board: 'Chessboard', from_c: 'Coord'):
    dummy_bishop = Bishop(self.color)
    dummy_rook = Rook(self.color)

    # A Queen's valid_moves is the union of a Bishop and a Rook's valid moves
    moves = dummy_bishop.valid_moves(board, from_c) \
      + dummy_rook.valid_moves(board, from_c)

    return moves

class King(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2654'
    return u'\u265a'

  def valid_moves(self, board: 'Chessboard', from_c: 'Coord'):
    moves = []

    # Enumerating possible moves clockwise, starting from north
    possible_targets = (
      (from_c.y - 1, from_c.x),
      (from_c.y - 1, from_c.x + 1),
      (from_c.y, from_c.x + 1),
      (from_c.y + 1, from_c.x + 1),
      (from_c.y + 1, from_c.x),
      (from_c.y + 1, from_c.x - 1),
      (from_c.y, from_c.x - 1),
      (from_c.y + 1, from_c.x - 1)
    )

    for t_y, t_x in possible_targets:
      if (Coord.is_in_bounds(t_y, t_x)
        and (board.empty_in(Coord(t_y, t_x)) or board.piece_in(Coord(t_y, t_x)).is_enemy(self))):
        moves.append(Move(from_c, Coord(t_y, t_x)))

    return moves