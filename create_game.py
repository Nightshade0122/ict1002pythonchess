import sys
import chess
import chess.board

def create_game():
    #Allow the user to paste the PGN via commandline or make moves via notation
    
    FEN = input("Paste FEN or enter for starting position")
    
    while not board.is_stalemate() and not board.is_insufficient_material() and not board.is_game_over():
        nextmove = input("Please enter next move in PGN notation")
            
        #Loop until user reaches checkmate
            break
        return 0
        
    else:
        print("Invalid input")
        create_game()
