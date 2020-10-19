import chess
import chess.pgn 

#search_criteria will look like {"Event":"Rated Classical Game","BlackElo":["1400","1500"]}
#Search through database using a criteria, search_criteria is a dict
def query_database(pgn, search_criteria):
    newpgn = []
    #Below are search criteria that can be a range
    range_search=["Date","BlackElo","WhiteElo","BlackRatingDiff","WhiteRatingDiff","UTCDate","UTCTime"]
    while True:                                     #Loop through all the games
        game = chess.pgn.read_game(pgn)
        if game is not None:                        #Check if games exists
            metCriteria = True
            for field in search_criteria:           #Loop through search criteria
                if field in range_search:
                    #Checks if game is in range of criteria
                    if not (game.headers[field] >= search_criteria[field][0] and game.headers[field] <= search_criteria[field][1]):
                        metCriteria = False
                        break                       #Criteria is not met, stop checking the game
                elif search_criteria[field] != game.headers[field]:
                    metCriteria = False
                    break                           #Criteria is not met, stop checking the game
            if metCriteria:                         #If game met criteria, add to newpgn
                newpgn.append(game)
        else:
            break                                   #If no more games are found, break the loop
    return newpgn

def enter_search():
    valid_fields = ["Event","Site","Round","White","Black","Result","ECO","Opening","Termination","TimeControl"]
    range_search=["Date","BlackElo","WhiteElo","BlackRatingDiff","WhiteRatingDiff","UTCDate","UTCTime"]
    search_criteria = {}
    print("Note that values are case sensitive!\nValid search fields:\n")
    print(valid_fields+range_search,"\n")
    while len(search_criteria)<18:                  #Total 17 fields
        field = input("Please input the search field (press enter to quit): ")
        if field == "":                             #Quit search entry
            break
        elif field not in valid_fields and field not in range_search:
            print("Invalid field entered!\n")       #Invalid field
            continue
        if field in range_search:                   #For fields that accept a range
            criteria = input("Please input the lower bound (press enter to go back): ")
            if criteria == "":                      #Back to entering search field
                print()
                continue
            criteria_2 = input("Please input the upper bound (press enter to go back): ")
            if criteria_2 == "":                    #Back to entering search field
                print()
                continue
            search_criteria[field] = [criteria,criteria_2]          #Assign value to dict
            print()
        else:                                       #For normal fields
            criteria = input("Please input the search criteria (press enter to go back): ")
            if criteria == "":                      #Back to entering search field
                print()
                continue
            else:
                search_criteria[field] = criteria   #Assign value to dict
                print()
    return search_criteria

def save_pgn(pgn,file_name):
    curr_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_path, file_name)
    with open(file_path, "w") as f:
        for game in pgn:
            f.write(str(game)+"\n\n")

#pgn = open("lichess_db_standard_rated_2013-01.pgn")
#newpgn = query_database(pgn,enter_search())
#save_pgn(newpgn,"Filtered Games.pgn")
