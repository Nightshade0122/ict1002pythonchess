import chess
import chess.pgn
import numpy as np
import matplotlib.pyplot as plt
import search
import statistics

def readfile(pgn):
    '''Read one pgn file only'''
    pgnlist=[]
    while True:
        game = chess.pgn.read_game(pgn)
        if game is not None:
            pgnlist.append(game)
        else:
            break
    return pgnlist
    
def getMovesCount(pgnlist):
    '''Get the chess moves in each game'''
    fulllist=[]
    for i in pgnlist: 
        fulllist.append(list(i.mainline_moves())) #Append move into a list
    move ={}
    movelist =[]
    for i in fulllist:
        movelist.append(int(len(i)/2))
    for i in movelist:
        move[i] = movelist.count(i)
    return move,movelist

def getMeanMedianMode(move,movelist):
    total = 0
    for i in move:
        total += int(i)
    mean = int(total/len(move)) #Average move make
    median = statistics.median(movelist)
    mode = statistics.mode(movelist)
    sort = sorted(move.items(),reverse=True)
    stat = {}
    stat["Mean"] = mean
    stat["Median"] = median
    stat["Mode"] = mode
    stat["Most Moves"] = sort[0][0]
    return stat
   
        
def getOpening(pgnlist):
    '''Get the opening used in all the games'''
    openingUsed = []
    for i in pgnlist:
       openingUsed.append(i.headers["Opening"]) #Append opening from each game
    opening ={}
    list1=[]
    for i in openingUsed: #Append data in to list
        try:
            a= i.split(":") #Only retrieve the word bef : eg. benoni Defense : Advance Variation
            list1.append(a[0])
        except IndexError:
            list1.append(i)
    for i in list1: #Append data into dictionary with its count
        opening[i] = list1.count(i)
    return opening

def getTimeControl(pgnlist):
    '''Get the time control used in each game'''
    timelist=[]
    timeControl={}
    for i in pgnlist:
        timelist.append(i.headers["TimeControl"]) #Append time control to list
    for i in timelist:
        timeControl[i] = timelist.count(i) #Append data to dictionary with value of its count.
    return timeControl


def terminationType(pgnlist):
    '''Get the data for different termination types'''
    termination ={}
    list1 =[]
    for i in pgnlist:
        list1.append(i.headers["Termination"])
    for i in list1:
        termination[i] = list1.count(i)
    return termination

    
    
def winRateWhiteBlack(pgnlist):
    '''Get the percentage of White wins, Black win and draw'''
    winrate={}
    white,black,draw =0,0,0
    count =0
    for i in pgnlist:
        count += 1
        if i.headers["Result"] == "1-0":
            white+=1
        elif i.headers["Result"] == "0-1":
            black+=1
        else:
            draw+=1
    winrate["White Wins"] = white/count*100
    winrate["Black Wins"] = black/count*100
    winrate["Draw"] =draw/count*100
    return winrate

def circleGraph(winrate):
    names =[]
    size=[]
    for i in winrate:
        names.append(str(round(winrate[i],2))+"% "+i)
        size.append(winrate[i])
    
    my_circle=plt.Circle( (0,0), 0.7, color='white')
    plt.pie(size, labels=names, colors=['red','green','blue'],wedgeprops = { 'linewidth' : 2, 'edgecolor' : 'white' })

    p=plt.gcf()
    plt.title("Percentage of White Wins, Black Wins and Draw")
    p.gca().add_artist(my_circle)
    plt.show()

     
def barGraph(x,col=5,title="",x_Label="",y_Label=""):
    '''This a  function generate a bar graph base on the list/ dictionary(x) given,
            Graph contains top 5 data by default, title and labels can be change.'''
    try:
        # Sort out top items
        sort = sorted(x.items(),key=lambda x: x[1], reverse=True)
        y_axis = []
        x_axis = []
        for i in range(0,col):
            y_axis.append(sort[i][1])
            x_axis.append(sort[i][0])

        y_pos = np.arange(len(x_axis))

        # Create bars
        plt.bar(y_pos, y_axis,width=0.5)

        # Create names on the x-axis
        plt.xticks(y_pos, x_axis)
        
        # Set margin
        plt.subplots_adjust(bottom=0.4, top=0.9)

        # Adding axis title and title
        plt.title(title)
        plt.xlabel(x_Label)
        plt.ylabel(y_Label)

        # Set lbel postion
        x_pos = []
        for i in range(len(x_axis)):
            x_pos.append(i)
            
        # Adding labels
        for i in range(len(x_axis)):
            plt.text(x = x_pos[i]-0.05,y=y_axis[i]+0.2, s = y_axis[i], size = 10)

        # Show graphic
        plt.show()
    except:
        print("\nError: Empty list found")

def datacount(data):
    '''Validation of the length input by user'''
    while True:
        count = int(input("Please enter the no. of data to be displayed: "))
        if count>1 and count < len(data):
            break
        else:
            print("Please enter a valid length")
            count = int(input("Please enter the no. of data to be displayed"))
    return count
            
    
    

def graphTypes(pgnlist):
    '''Selection of graphs'''
    if len(pgnlist) != 0:
        while True:
            print("\n------------------------------Welcom to Analytics--------------------------------")
            print("\nEnter 1 to display bar chart of Top Opening used")
            print("Enter 2 to display bar chart of  Termination Types used")
            print("Enter 3 to display bar chart of Most common Time Control used")
            print("Enter 4 to display chart of Winning rate of Black and White")
            print("Enter 5 to display chart Mean, Median and Mode of the no. of Moves")           
            print("Enter 0 to Exit\n----------------------------------------------------------------------------------------")

            choice = int(input("\nPlease enter Graph option: "))
            
            if 0 <= choice <= 5:
                if choice == 0:
                    break
                elif choice == 1: #Display bar chart of Top 5 Opening used
                    opening = getOpening(pgnlist)
                    length = datacount(opening)
                    newtitle  = "Top "+ str(length) + " Opening"
                    barGraph(opening,length,newtitle,"Type of Openings","No. of Times")
                elif choice == 2: # Display bar chart of Top 5 Opening move used
                    types = terminationType(pgnlist)
                    barGraph(types,len(types),"Count of Different Termination Used","Type of Termination","Frequency")
                elif choice == 3: # Display bar chart of Top 5 Time Control used
                    timeControl=getTimeControl(pgnlist)
                    length = datacount(timeControl)
                    barGraph(timeControl,length,"Most Common Time Control Used","Type of Time Control","No. of Times")
                elif choice ==4: #Display the winning rate of black and white
                    winrate=winRateWhiteBlack(pgnlist)
                    circleGraph(winrate)
                elif choice == 5: #Display the mean median and mode of the moves in every game 
                    move,movelist = getMovesCount(pgnlist)
                    stat=getMeanMedianMode(move,movelist)
                    barGraph(stat,len(stat),"Mean, Median and Mode of No. of Move make","","No. of moves")
                    
            else:
                print("\nPlease enter  a valid option")
                choice = int(input("Please enter Graph option: "))
    else:
        print("Empty list found")
            



#pgn = open("database/small.pgn")
#pgnlist=readfile(pgn)

#graphTypes(pgnlist)














    











