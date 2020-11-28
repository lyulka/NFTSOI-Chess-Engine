from chessboard import Chessboard
from coord import Coord
from move import Move
from test import dynamic_move_test

LONGFORM_COLOR = {
  'w': 'White',
  'b': 'Black'
}

class AI:
  def __init__(self, color: str):
    self.color = color

  """
  Minimax algorithm with Alpha-Beta Pruning.

  White is the maximizer.
  Black is the minimizer. 
  """
  def get_best_position(self, board: Chessboard, color,
    depth: int=0, alpha: float=float("-inf"), beta: float=float("+inf")):
    if depth == 4: # Depth limit ADD CHECKMATE DETECTION
      return board.evaluate(), None
    else:

      if color == "w":
        best_position = None
        for candidate in board.legal_positions(color):
          score, _ = self.get_best_position(candidate, "b",
            depth + 1, alpha, beta)
          
          # Move that Black would take in response to this move has higher
          # score than the previous score assured for White.
          if score > alpha:
            alpha = score
            best_position = candidate

            # Alpha-Beta cutoff. The maximum score assured to Black is
            # less than the minimum score assured to White. A minimizing
            # Black will never go down this (upper) branch. It'll just
            # go down the maximum (beta) guaranteed branch assured to
            # it.
            if alpha >= beta:
              break
        
        return (alpha, best_position)

      else: # color:
        best_position = None
        for candidate in board.legal_positions(color):
          score, _ = self.get_best_position(candidate, "w",
            depth + 1, alpha, beta)

          # Move that White would take in response to this move has lower
          # score than the previous score assured for Black.
          if score < beta:
            beta = score
            best_position = candidate

            # Alpha-Beta cutoff. The minimum score assured to White is
            # more than the maximum score assured to Black. A minimizing
            # White will never go down this (upper) branch. It'll just
            # go down the minimum (alpha) guaranteed branch assured to it.
            if alpha >= beta:
              break

        return (beta, best_position)

class Game:
  def __init__(self):
    self.board = Chessboard()
    self.human_color = None
    self.AI = None
    
    # Stores sequence of moves made from start to finish.
    # self.moves[-1] is the latest move made so far, so
    # the array is initialized to [None] (no moves made so
    # far.)
    self.moves = [None]

  def start(self):
    print("Prince's Chess v0.1")
    self.human_color = input("Choose your color (B or W): ").lower()
    self.AI = AI('w' if self.human_color == 'b' else 'b')
    
    # Render player's side at the bottom
    vertical_flip = self.human_color == 'b'
    
    while True:

      #
      # PLAYER'S TURN
      #
      self.board.print_board(self.moves[-1], vertical_flip=vertical_flip)

      print("Enter a move")
      from_square = input("Piece: ").lower()
      to_square = input("To: ").lower()

      if (not Coord.is_in_bounds(a_n=from_square)
        or not Coord.is_in_bounds(a_n=to_square)):
        print("You are going out of bounds with those coordinates!")
        continue

      from_coord = Coord(a_n=from_square)
      to_coord = Coord(a_n=to_square)
      move = Move(from_coord, to_coord)

      dynamic_move_test(self.board, self.board.piece_in(from_coord), 
        self.human_color, from_coord)

      is_valid = Move.is_valid(self.board, self.human_color, move)

      if (not is_valid):
        print("That was a nonsensical move.")
        continue

      move = Move(from_coord, to_coord)
      new_position = self.board.make_move(move)

      if new_position.is_check(self.human_color):
        print("That was an illegal move.")
        continue
      
      self.moves.append(move)
      self.board = new_position

      if self.board.is_checkmate(self.AI.color):
        print(f"{LONGFORM_COLOR[self.human_color]} Wins! You win!")
        break

      #
      # AI's TURN
      #
      self.board.print_board(self.moves[-1], vertical_flip=vertical_flip)
      print("AI is thinking...")

      score, position = self.AI.get_best_position(self.board, self.AI.color, 0)
      print(f"score: {score}")
      self.board = position

      if self.board == None or self.board.is_checkmate(self.human_color):
        print(f"{LONGFORM_COLOR[self.AI]} Wins! AI wins!")

g = Game()
g.start()
