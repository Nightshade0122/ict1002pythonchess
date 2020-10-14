import chess.pgn
import time
from chessboard import display

def GUI(game):                              #Opens the GUI to run the game
        for move in game.mainline_moves():
                board.push(move)
                time.sleep(1)
                display.start(board.fen())
        display.terminate()
    
 
