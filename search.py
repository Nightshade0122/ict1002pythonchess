import chess
import chess.pgn 

#Search through database using a criteria, search_criteria is a dict
def query_database(pgn, search_criteria):
    newpgn = []
    while True:                                     #Loop through all the games
        game = chess.pgn.read_game(pgn)
        if game is not None:                        #Check if games exists
            metCriteria = True
            for field in search_criteria:           #Loop through search criteria
                if search_criteria[field] != game.headers[field]:
                    metCriteria = False
                    break                           #Criteria is not met, stop checking the game
            if metCriteria:                         #If game met criteria, add to newpgn
                newpgn.append(game)
                print(game)                         #Print to demo it working
        else:
            break                                   #If no more games are found, break the loop
    return newpgn

#pgn = open("database/lichess_db_standard_rated_2013-01.pgn")
#search_criteria = {"Event":"Rated Classical game","Result":"1-0"}
#newpgn = query_database(pgn,search_criteria)
