import sys
import chess
import chess.board

def create_game():
    #Allow the user to paste the PGN via commandline or make moves via notation
    userinput = input("Enter game via PGN or move-by-move?")
    if userinput in "PGN":                      #If user chooses to paste in the game's full PGN
        while True:
            print("Please paste PGN:")          
            lines = []
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break
            userpgn = '\n'.join(lines)
            print(userpgn)
            game = chess.pgn.read_game(userpgn)
            break
    elif userinput in "move":
        FEN = input("Paste FEN or enter for starting position")
        
        while not board.is_stalemate() and not board.is_insufficient_material() and not board.is_game_over():
            nextmove = input("Please enter next move in PGN notation")
            
            #Loop until user reaches checkmate
            break
        return 0
        
    else:
        print("Invalid input")
        create_game()
