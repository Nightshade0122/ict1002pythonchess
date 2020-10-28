import sys
import os
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
        print("1. search \n2. create game \n3. analytics \n4. machinelearning\n")
        enterinput = input()
        if enterinput in "search":             #Search option selected
            searchcriteria = search.enter_search()      #Asks user for search criteria
            showfirstgame = True
            pgnresult = []
            print("Please wait, searching through database...")
            for i in range(len(databaselist)):
                pgnresult += search.query_database(databaselist[i],searchcriteria)  #Store filtered results
                if showfirstgame:              #Show the first game found in GUI
                    showfirstgame = False
                    try:
                        try:
                            gui(pgnresult[0])
                        except:     #If GUI fails to display, use database_games to show every game in command-line
                            database_games(pgnresult[0], showpgn=False, cmdboard=True)
                    except IndexError:
                        print("Search found no games within the database!")
            break
        elif enterinput in "analytics":
            pgnlist = analytic.getlist(databaselist)
            analytic.graphTypes(pgnlist)
            break
        else:
            print("Invalid input")

#databaselist = read_database("database")
#database_games(databaselist[0], showpgn=False, cmdboard=True)           #Prints all the game PGNs in the database

if __name__ == "__main__":
    main()
