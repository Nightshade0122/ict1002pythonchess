import sys
import os
import io
from os.path import join
import chess
import chess.pgn
import chess.svg
import evaluate
import search
import gui
import analytic

def read_database(database):                    #Read from a database directory and return the PGN
    pgn = []
    try:
        for i in os.listdir(database):
            pgn.append(open(join(database, i))) #Loop through database for files
    except:
        return None                             #Database cannot be found
    return pgn                                  #Return database as text I/O wrapper in list

def database_games(pgn, showpgn=False, cmdboard=False):     #Loop through all the games in the PGN using text I/O wrapper
    #Chess database can be in PGN
    #'showpgn' determines if game's PGN is printed (default: False)
    #'cmdboard' determines if game is printed on the command line board (default: False)
    total = 1                                   #To count the number of games in the database
    try:
        while True:
            game = chess.pgn.read_game(pgn)     #Read games from PGN
            if game is not None:                #Check if game exists
                if showpgn:
                    print(game)                 #Print out the game(s) in PGN
                if cmdboard:
                    command_line_board(game)    #Print through every game(s)
                total = total + 1
            else:
                break                           #If no more games are found, break the loop and return
        return total                            #Return total number of games found
    except:
        return 0                                #No games found due to an error

def command_line_board(game, FEN=False):        #Showing the game moves in command line
    #'FEN' determines if FEN notation is printed along with board (default: False)
    #Used if GUI cannot be displayed
    if game is None: #Used to create a game via command line
        game = chess.pgn.Game()
        while True:                             #Infinite loop to get the
            userinput = input("Paste FEN or enter for default starting position:")
            if userinput == "":
                board = chess.Board()           #Default starting chess position
                break
            if userinput == "exit":             #Exit this function
                return None
            else:
                try:
                    board = chess.Board(userinput)  #User keys in FEN notation
                    break
                except:
                    print("Invalid FEN!")
        game.setup(board)                       #Add the board position to the game
        x = 0
        movelist = []
        while True:
            #Show board state
            print("---------------")
            print(board)
            print("---------------")
            if board.is_stalemate():
                print("Stalemate!")             #If game ends in stalemate
                break
            if board.is_game_over():             #If the game ends in any way (stalemate, checkmate, repetition,
                print("Game over!")
                break

            nextmove = input("Please key in the next move or undo:")
            if nextmove == "undo":
                board.pop()
            try:
                if x == 0:
                    node = game.add_main_variation(board.push_san(nextmove))
                    x = x + 1
                else:
                    node = node.add_main_variation(board.push_san(nextmove))
            except ValueError:
                print("Invalid move given!")
        return game


    try:
        board = game.board()                    #Starting board state is assigned
        counter = 1                             #To count the move numbers when printing to user
        for move in game.mainline_moves():
            if counter%2 == 1:
                print("%d :" %(counter/2 + 1), end ='')
                print("%s" %board.san(move)) #To signify that it is White's move and convert to PGN notation
                counter = counter + 1
            elif counter%2 == 0:
                print("%d :... " %(counter/2), end ='')
                print("%s" %board.san(move)) #To signify that it is Black's and convert to PGN notation
                counter = counter + 1

            board.push(move)                    #Make next move in game
            if FEN:
                print(board.fen())              #Show FEN notations with the board
            #Show board state
            print("---------------")
            print(board)
            print("---------------")
            if input() == "":                   #Enter to show next move and board state
                continue
        return board.fen()                      #Returns the final position of the game in FEN
    except:
        return False                            #Game could not be displayed in command-line

def main():
    chessdatabase = "database"                  #Name of directory containing all databases
    databaselist = read_database(chessdatabase) #Creates list of I/O wrappers for all databases listed
    print("Initialization complete!")

    while True:
        print()
        print("Please select from the options:")
        print("1. Search \n2. Create game \n3. Analytics \n4. Display game\n5. Exit")
        enterinput = input()
        if enterinput in "1":             #Search option selected
            searchcriteria = search.enter_search()      #Asks user for search criteria
            showfirstgame = True
            pgnresult = []
            print("Please wait, searching through database...")
            for i in range(len(databaselist)):
                pgnresult += search.query_database(databaselist[i],searchcriteria)  #Store filtered results
                if showfirstgame:              #Show an example game found in the GUI
                    showfirstgame = False
            search.save_pgn(pgnresult,"FilteredGames.pgn")
            print("Export complete! Results are stored in database/FilteredGames.pgn")
            break
        elif enterinput in "2": #Create game
            try:
                import gui_pgn
            except:
                command_line_board(None, False)
        elif enterinput in "3":
            pgnlist = analytic.getlist(databaselist)
            analytic.graphTypes(pgnlist)
            break
        elif enterinput in "4":
            try:
                try:
                    game = chess.pgn.read_game(databaselist[0])
                    gui.gui(game)
                except:     #If GUI fails to display, use database_games to show every game in command-line
                    database_games(game, showpgn=False, cmdboard=True)
            except IndexError:
                print("Search found no games within the database!")
        elif enterinput in "5":
            print("Exiting program")
            break
        else:
            print("Invalid input")

#databaselist = read_database("database")
#database_games(databaselist[0], showpgn=False, cmdboard=True)           #Prints all the game PGNs in the database
#print(command_line_board(None, False))
if __name__ == "__main__":
    main()
