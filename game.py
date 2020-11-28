from chessboard import Chessboard
from coord import Coord
from move import Move
from test import dynamic_move_test

import multiprocessing as mp
import time

LONGFORM_COLOR = {
  'w': 'White',
  'b': 'Black'
}

class AI:
  def __init__(self, color: str):
    self.color = color

  def get_best_position_ID(self, board: Chessboard, color, return_queue: mp.Queue):

    depth_limit = 0
    
    while True:
      depth_limit += 1
      print(f"Depth limit = {depth_limit}")
      score, best_position = self.get_best_position(board, color, 0, depth_limit)
      return_queue.put([score, best_position])

    return
    
  """
  Minimax algorithm with Alpha-Beta Pruning.

  White is the maximizer.
  Black is the minimizer. 
  """
  def get_best_position(self, board: Chessboard, color,
    depth: int, depth_limit: int, alpha: float=float("-inf"), beta: float=float("+inf")):

    if depth == depth_limit:
      return board.evaluate(), None

    else:

      if color == "w":
        best_position = None
        for candidate in board.legal_positions(color):
          score, _ = self.get_best_position(candidate, "b",
            depth + 1, depth_limit, alpha, beta)
          
          # Move that Black would take in response to this move has higher
          # score than the previous score assured for White.
          if score > alpha:
            alpha = score
            best_position = candidate

            # Alpha-Beta cutoff. The maximum score assured to Black is
            # less than the minimum score assured to White. Black will
            # never allow white to reach this position.
            if alpha >= beta:
              break
        
        return (alpha, best_position)

      else: # color: 'b'
        best_position = None
        for candidate in board.legal_positions(color):
          score, _ = self.get_best_position(candidate, "w",
            depth + 1, depth_limit, alpha, beta)

          # Move that White would take in response to this move has lower
          # score than the previous score assured for Black.
          if score < beta:
            beta = score
            best_position = candidate

            # Alpha-Beta cutoff. The minimum score assured to White is
            # more than the maximum score assured to Black.
            if alpha >= beta:
              break

        return (beta, best_position)

class Game:
  def __init__(self):
    self.board = Chessboard()
    self.time_limit = 1
    self.human_color = None
    self.AI = None

  def config(self):
    print("Prince's Chess (named after my dog!)")

    while True:
      print("### Game Configuration ###")

      try:
        self.time_limit = float((input("For how many seconds should the CPU player think? (in secs): ")))
        if self.time_limit < 2:
          print("Please enter a number greater than 2.")
          continue

        # A limitation of this program as it stands is that the human
        # player MUST play white.
        self.human_color = 'w'
        self.AI = AI('b')
        break

      except KeyboardInterrupt:
        print()
        return

      except:
        print("You inputted a really, really weird value")
        continue

    self.start()
        
  def start(self):
    print("### Game START ###")
    print("White: You, Black: CPU")
    
    # Render player's side at the bottom
    vertical_flip = self.human_color == 'b'
    
    while True:

      #
      # PLAYER'S TURN
      #
      self.board.print_board(vertical_flip=vertical_flip)

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

      # FOR MOVE GENERATOR DEBUGGING #
      # dynamic_move_test(self.board, self.board.piece_in(from_coord), 
      #   self.human_color, from_coord)

      is_valid = Move.is_valid(self.board, self.human_color, move)

      if (not is_valid):
        print("That was a nonsensical move.")
        continue

      move = Move(from_coord, to_coord)
      new_position = self.board.make_move(move)

      if new_position.is_check(self.human_color):
        print("That was an illegal move.")
        continue
      
      self.board = new_position

      if self.board.is_checkmate(self.AI.color):
        print(f"{LONGFORM_COLOR[self.human_color]} Wins! You win!")
        return

      self.board.print_board(vertical_flip=vertical_flip)

      #
      # AI's TURN
      #
      print("CPU is thinking...")

      return_queue = mp.Queue()
      ID_worker = mp.Process(target=self.AI.get_best_position_ID,
        args=(self.board, self.AI.color, return_queue))
      ID_worker.start()

      start = time.perf_counter()

      time.sleep(self.time_limit)
      ID_worker.terminate()

      end = time.perf_counter()

      depth_achieved = 0
      while not return_queue.empty():
        depth_achieved += 1
        score, best_position = return_queue.get()
      
      print(f"Achieved depth {depth_achieved} in {end - start:.1f} seconds with Iterative Deepening")
      print(f"Score: {score}")

      self.board = best_position

      if self.board is None or self.board.is_checkmate(self.human_color):
        print(f"{LONGFORM_COLOR[self.AI.color]} Wins! AI wins!")
        return

g = Game()
g.config()
