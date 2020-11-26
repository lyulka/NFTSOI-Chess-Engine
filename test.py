from chessboard import Chessboard
from pieces import *
from coord import Coord
from move import Move

def move_is_valid(board: Chessboard, color: str, from_coord: Coord, to_coord: Coord):
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
          and to_coord.x == from_coord.x
          and board.empty_in(Coord(from_coord.y - 1, from_coord.x))):
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
          and to_coord.x == from_coord.x
          and board.empty_in(Coord(from_coord.y + 1, from_coord.x))):
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


# Test if all moves generated by valid_moves functions are actually valid.
board = Chessboard()

tests = (
  (board.piece_in((Coord(6, 0))), 'w', Coord(6, 0), "White side pawn"),
  (board.piece_in((Coord(6, 2))), 'w', Coord(6, 2), "White center pawn"),
  (board.piece_in((Coord(1, 0))), 'b', Coord(1, 0), "Black side pawn"),
  (board.piece_in((Coord(1, 2))), 'b', Coord(1, 2), "Black center pawn"),
  (board.piece_in((Coord(7, 1))), 'w', Coord(7, 1), "White west knight"),
  (board.piece_in((Coord(7, 6))), 'w', Coord(7, 6), "White east knight"),
  (board.piece_in((Coord(0, 1))), 'b', Coord(0, 1), "Black west knight"),
  (board.piece_in((Coord(0, 6))), 'b', Coord(0, 6), "Black east knight")
)

if __name__ == '__main__':
  for piece, color, coord, desc in tests:
    print(f"Testing: {desc}")
    valid_moves = piece.valid_moves(board, coord)
    for move in valid_moves:
      try:
        is_valid, reason = move_is_valid(board, color, move.from_coord, move.to_coord)
        assert is_valid
        print(f"{move} " + u"\u2713")
      except (AssertionError):
        print(f"{move} " + u"\u2717" + f" {reason}")


# Test whilst playing the game
def dynamic_move_test(board: 'Board', piece: 'Piece', color: 'str', coord: 'Coord'):
  if type(piece) == Empty:
    return

  valid_moves = piece.valid_moves(board, coord)
  for move in valid_moves:
    try:
      is_valid, reason = move_is_valid(board, color, move.from_coord, move.to_coord)
      assert is_valid
      print(f"{move} " + u"\u2713")
    except (AssertionError):
      print(f"{move} " + u"\u2717" + f" {reason}")