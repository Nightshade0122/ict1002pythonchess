import chess
import chess.engine

def evaluate(boardFEN, turn='0', time=500, engine="stockfish"):   #Evaluates the board state, default White
    
    #'turn' determines whose turn it is (default: 0 -> White)
    #'time' determines the time engine spends thinking in milliseconds (default: 100ms)
    #engine 

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
    
    engine = chess.engine.SimpleEngine.popen_uci("engines/stockfish_20090216_x64_bmi2.exe")

    time = time/1000
    board = chess.Board(boardFEN)
    info = engine.analyse(board, chess.engine.Limit(time=time))
    print(board)

    engine.quit()

    return (info["score"])
    
def best_move(boardFEN):
    return 0


#board1 = "r1bqkbnr/p1pp1ppp/1pn5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 2 4"
#print(evaluate(board1))
