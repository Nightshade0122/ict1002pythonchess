import sys
import os
from os.path import join
import chess
import chess.pgn
import chess.svg
#import evaluate
#import search

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
        for move in game.mainline_moves():
            board.push(move)                    #Make next move in game
            if FEN:
                print(board.fen())              #Show FEN notations with the board
            #Show board state
            print("---------------")
            print(board)                    
            print("---------------")
        return board.fen()                      #Returns the final position of the game in FEN
    except:
        return False                            #Game could not be displayed in command-line

#Search through database using a criteria
def query_database(pgn, searchcriteria, searchvalue): 
    newpgn = Null                               #Search value
    return newpgn


chessdatabase = "database"                      #Name of directory containing all databases
databaselist = read_database(chessdatabase)     #Creates list of I/O wrappers for all databases listed
#database_games(databaselist[0])                #Prints all the game PGNs in the database

