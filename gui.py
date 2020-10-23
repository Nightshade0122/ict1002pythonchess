import chess.pgn
import chess.svg
import sys
import qdarkstyle
from lib.PyQt5 import QtSvg, QtGui
from lib.PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView


def writefile(board):   #Convert svg from chess library to a svg file
    boardsvg = chess.svg.board(board=board)
    f = open("Images/Board.svg", "w")
    f.write(boardsvg)
    f.close()


def next_button_clicked(event): #move the piece if the next button is pressed
    global i
    if i < len(move_list):  #if counter i is less than the length of move_list, move the piece and create the svg file
        board.push(move_list[i])
        writefile(board)
        i += 1
        board_widget.load("Images/board.svg")   #Refresh the board widget
    else:
        pass


def previous_button_clicked(event): #undo the move if the previous button is pressed
    global i
    if i > 0: #if counter i is more than 0, undo the move and create the svg file
        i -= 1
        board.pop()
        writefile(board)
        board_widget.load("Images/board.svg")   #Refresh the board widget
    else: 
        pass


def generate_move_list(game):   #generate a list of all moves
    move_list = []
    for move in game.mainline_moves():
        move_list.append(move)
    return move_list


def set_table_content(move_list):    #set all the moves into the table 
    count = 0
    for move in move_list:
        tableWidget.setItem(count, 0, QTableWidgetItem("Move.from_uci(" + str(move) + ")"))
        count += 1


def gui(game):
    global i, board_widget, tableWidget, board, move_list
    i = 0
    board = game.board()
    writefile(board)
    move_list = generate_move_list(game) 

    app = QApplication(sys.argv)    #initialise the pyqt application
    app.setStyleSheet(qdarkstyle.load_stylesheet()) #load third party dark theme
    main_layout = QVBoxLayout()     #set main layout to have a Vertical layout
    upper_section = QHBoxLayout()   #set upper section to have a Horizontal layout
    lower_section = QHBoxLayout()

    window = QWidget()  #initialise main window widget
    tableWidget = QTableWidget()    #initialise table widget
    tableWidget.setRowCount(len(move_list)) #set the no of rows for the table
    tableWidget.setColumnCount(1)   #set the no of columns for the table
    tableWidget.setHorizontalHeaderLabels(["Chess Moves"]) #set column name for the table
    header = tableWidget.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  #resize column to fit the content perfectly
    set_table_content(move_list)     #set table content using the move list generated
    board_widget = QtSvg.QSvgWidget('Images/Board.svg')    #initialise board widget

    upper_section.addWidget(board_widget)   #add the widgets to the upper section
    upper_section.addWidget(tableWidget)

    previous_button = QPushButton() #create a push button for previous move
    previous_button.setToolTip("Previous move") 
    previous_button.setIcon(QtGui.QIcon("Images/left-arrow.png")) 
    previous_button.clicked.connect(previous_button_clicked)    #create a event handler for the previous button
    next_button = QPushButton() #create a push button for next move
    next_button.setToolTip("Next move")
    next_button.setIcon(QtGui.QIcon("Images/right-arrow.png"))
    next_button.clicked.connect(next_button_clicked)     #create a event handler for the next button

    lower_section.addWidget(previous_button)    #add the previous button to the lower section
    lower_section.addWidget(next_button)        #add the next button to the lower section

    main_layout.addLayout(upper_section)        #add the upper section layout to the main_layout
    main_layout.addLayout(lower_section)        #add the lower section layout to the main_layout
    window.setLayout(main_layout)               #set the main layout for the main widget
    window.setWindowTitle("Chess Board")       #set the window title
    window.show()                               #show main window widget
    sys.exit(app.exec_())
    
    
#pgn = open("lichess_db_standard_rated_2013-01.pgn")
#game = chess.pgn.read_game(pgn)
#gui(game)


