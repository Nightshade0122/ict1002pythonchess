import chess
import chess.engine
import chess.pgn
from chess.engine import Cp

def engine_name(engine):
    #Find a suitable engine uci file based on the name in '/engines" directory
    file = "engines/"                                   #Directory of engines
    try:
        if "stockfish" in engine:                       #Stockfish engine selected
            return file + "stockfish_20090216_x64_bmi2.exe" 
        elif "komodo" in engine:                        #Komodo engine selected
            return file + "komodo-11.01-64bit.exe"
        elif "fire" in engine:                          #Fire engine selected
            return file + "Fire_7.1_x64_popcnt.exe"
        else:
            return None #A suitable engine could not be found
    except: #Engine was not found
        return None

def evaluate(boardFEN, turn='0', time=5000, enginename="stockfish"):   #Evaluates the board state, default White
    #'turn' determines whose turn it is (default: 0 -> White)
    #'time' determines the time engine spends thinking in milliseconds (default: 500ms = 0.5s)
    #'engine' determines the name of engine to be used (default: 100ms)

    #The higher the return value the better it is for White
    #The lower the return value the better it is for Black
    #Positive means good for White
    #Negative means good for Black
    if turn == 0:                       #White's turn
        playerturn = chess.WHITE
    elif turn == 1:                     #Black's turn
        playerturn = chess.BLACK
    else: #If turn is somehow not 0 or 1, assume White's turn
        return evaluate(boardFEN, 0)

    time = time/1000                    #Calculate time in seconds
    board = chess.Board(boardFEN)
    
    if engine_name(enginename) is None: #Name of the engine was undefined
        return False #Returns False when error
    try:
        engine = chess.engine.SimpleEngine.popen_uci(engine_name(enginename)) #Opens the engine
        info = engine.analyse(board, chess.engine.Limit(time=time)) #Sets the time given to engine for evaluation
        
    except:
        print("No engine found!")
        return False #Returns False when error

    if board.is_stalemate() or board.is_insufficient_material() or board.is_game_over(): #If it is impossible for the engine to make any meaningful progress
        return None #Returns None because it is not possible to create any meaningful progress
    
    if(info["score"].is_mate()):                #Check if engine found mate
        centipawn = info["score"]
        engine.quit()
        return centipawn                    #If mate is found, returns the game as well
    else: #No mate found
        centipawn = (info["score"].white().score())/100 #To get the centipawn value
    engine.quit()
    return centipawn
    
def find_mate(boardFEN): #Should only be used if mate is possible
    board = chess.Board(boardFEN)
    engine = chess.engine.SimpleEngine.popen_uci(engine_name("stockfish"))
    info = engine.analyse(board, chess.engine.Limit(depth=20)) #Limit the possible checkmate found to be under 20 moves
    
    board_states = []                   #List of every board state in FEN notation during mate
    board_states.append(boardFEN)

    game = chess.pgn.Game()
    game.setup(boardFEN)
    x = 0
    if not (info["score"].is_mate()):
        engine.quit()
        return None #The score given is not a mate, therefore, the function cannot return a mate. Therefore, it returns None
    for i in info["pv"]:                    #Loop through every move and add them to the lists
        if x == 0:
            node = game.add_main_variation(i) #If first loop, create the main line found by engine
            x = x + 1 
        else:
            node = node.add_main_variation(i) #Add to the main line if not first loop
        board.push(i)
        board_states.append(board.fen())        #Add the FEN board state after the move was made
    engine.quit()
    return game 

#Board positions for testing
#board1 = "r1bqkbnr/p1pp1ppp/1pn5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 2 4"
#print(evaluate(board1))
#print(find_mate(board1))
#board2 = "B1N1q3/1P1p4/4P1p1/1RP1P1P1/8/BPp2p2/pP3P2/RNk1K3 w Q - 0 34"
#print(evaluate(board2))
#print(find_mate(board2))
#board3 = "5r2/8/1R6/ppk3p1/2N3P1/P4b2/1K6/5B2 w - - 0 1"            #Super hard puzzle, correct move is Rxb5+ !!
#print(evaluate(board3))
#print(get_mate(board3))
#board4 = "5rk1/pp1b2p1/4p2p/3p2p1/3P4/1P2P3/P3nPPP/R1R3K1 w - - 2 25"
#print(evaluate(board4))
#board5 = "r2q1rk1/pppb1ppB/2nb1n2/3p2B1/3P4/2N1P3/PPQ2PPP/R3K1NR b KQ - 0 9"
#print(evaluate(board5))
#board6 = "8/8/8/8/pr1R4/k7/8/2K5 w - - 0 100"
#print(evaluate(board6))
