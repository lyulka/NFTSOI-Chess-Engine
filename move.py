from coord import Coord

class Move:
  def __init__(self, from_coord: Coord, to_coord):
    self.from_coord = from_coord
    self.to_coord = to_coord

  def __str__(self):
    return f"Move: {self.from_coord} -> {self.to_coord}"

  def __eq__(self, other: 'Move'):
    return self.from_coord == other.from_coord \
      and self.to_coord == other.to_coord

  @staticmethod
  def is_valid(board: 'Chessboard', color: str, move: 'Move'):
    # Player tries to move an empty square
    if board.empty_in(move.from_coord):
      return False

    # Player tries to move piece that they do not own
    if board.piece_in(move.from_coord).color != color:
      return False

    # The piece simply cannot make such a move
    if not move in board.piece_in(move.from_coord).valid_moves(board, move.from_coord):
      return False

    return True


