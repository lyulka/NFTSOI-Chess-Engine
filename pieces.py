from chessboard import *

class Empty:
  def __str__(self):
    return u'\u25c7'

class Piece:
  def __init__(self, color):
    self.color = color

class Pawn(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2659'
    return u'\u265f'

  # Valid move generation is used strictly to generate moves
  # for the AI player. The validity of moves inputted by the
  # human player is checked in Move.is_valid.
  # def valid_moves(self, coords: tuple):
  #   res = []

  #   # The pawn is in its starting position.
  #   if (coords[1] == 1 or coords[1] )


class Knight(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2658'
    return u'\u265e'

class Bishop(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2657'
    return u'\u265d'

class Rook(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2656'
    return u'\u265c'

class Queen(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2655'
    return u'\u265b'

class King(Piece):
  def __str__(self):
    if self.color == 'b': return u'\u2654'
    return u'\u265a'