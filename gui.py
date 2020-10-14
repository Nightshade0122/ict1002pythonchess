def GUI(game):                              #Opens the GUI to run the game
        for move in game.mainline_moves():
                board.push(move)
                time.sleep(2)
                display.start(board.fen())
    
 
