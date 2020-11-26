from chessboard import *

class AI:
  def __init__(self, color: str):
    self.color = color

  """
  Minimax algorithm with Alpha-Beta Pruning.

  White is the maximizer.
  Black is the minimizer. 
  """
  def get_best_move(self, board: Chessboard, color: str, 
    depth: int, alpha: float=float("-inf"), beta: float=float("+inf")):
    if depth == 5: # Depth limit
      return (board.evaluate(), None)
    else:

      if color == "w":
        best_move = None
        for successor_position in board.legal_positions():
          score, move = self.get_best_move(successor_position, color, depth + 1, alpha, beta)
          
          # Move that Black would take in response to this move has higher
          # score than the previous score assured for White.
          if score > alpha:
            alpha = score
            best_move = move

            # Alpha-Beta cutoff. The maximum score assured to Black is
            # less than the minimum score assured to White. A minimizing
            # Black will never go down this (upper) branch. It'll just
            # go down the maximum (beta) guaranteed branch assured to
            # it.
            if beta < alpha:
              break
        
        return (alpha, best_move)

      else: # self.color == "b":
        best_move = None
        for successor_position in board.legal_positions():
          score, move = self.get_best_move(successor_position, color, depth + 1, alpha, beta)

          # Move that White would take in response to this move has lower
          # score than the previous score assured for Black.
          if score < beta:
            beta = score
            best_move = move

            # Alpha-Beta cutoff. The minimum score assured to White is
            # more than the maximum score assured to Black. A minimizing
            # White will never go down this (upper) branch. It'll just
            # go down the minimum (alpha) guaranteed branch assured to it.
            if alpha > beta:
              break

        return (beta, best_move)


class Game:
  def __init__(self):
    self.board = Chessboard()
    self.color = None
    self.AI = None
    
    # Stores sequence of moves made from start to finish.
    # self.moves[-1] is the latest move made so far, so
    # the array is initialized to [None] (no moves made so
    # far.)
    self.moves = [None]

  def start(self):
    print("Prince's Chess v0.1")
    self.color = input("Choose your color (B or W): ").lower()
    self.AI = AI('w' if self.color == 'b' else 'b')
    
    # Render player's side at the bottom
    vertical_flip = self.color == 'b'
    
    while (not self.board.get_victor()):

      # Player's turn
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

      is_valid, reason = Move.is_valid(self.board, self.color, from_coord, to_coord)

      if (not is_valid):
        print("That was a nonsensical move.")
        print(reason)
        continue

      move = Move(from_coord, to_coord)
      new_position = self.board.make_move(move)

      # if (not new_position.is_check()):
      #   print("That was an illegal move.")
      #   continue
      
      self.moves.append(move)
      self.board = new_position

      
      # AI's turn
      # self.board.print_board(self.moves[-1], vertical_flip=vertical_flip)
      # print("AI is thinking...")

      # move = self.AI.get_best_move(self.board)
      # new_position = self.board.make_move(move)

g = Game()
g.start()
