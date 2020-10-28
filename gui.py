import chess.pgn
import chess.svg
import sys
import qdarkstyle
import evaluate
import copy
from PyQt5 import QtSvg, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, \
    QTableWidgetItem, QAbstractScrollArea, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import pyqtSlot
import io

input_move_list = []
final_move_list = []
final_evaluation_list = []
text = ""
input_text = "0"


def writefile(board):  # Convert svg from chess library to a svg file
    boardsvg = chess.svg.board(board=board)
    f = open("Images/Board.svg", "w")
    f.write(boardsvg)
    f.close()


def next_button_clicked(event):  # move the piece if the next button is pressed
    global i, final_move_list
    if i < len(final_move_list):  # if counter i is less than the length of move_list, move the piece and create the svg file
        board.push(board.parse_san(final_move_list[i]))
        writefile(board)
        i += 1
        board_widget.load("Images/board.svg")  # Refresh the board widget
    else:
        pass


def previous_button_clicked(event):  # undo the move if the previous button is pressed
    global i
    if i > 0:  # if counter i is more than 0, undo the move and create the svg file
        i -= 1
        board.pop()
        writefile(board)
        board_widget.load("Images/board.svg")  # Refresh the board widget
    else:
        pass


def generate_move_and_eval_list(game):  # generate a list of all moves
    move_list = []
    evaluation_list = []
    temp_board = copy.copy(board)
    for move in game.mainline_moves():
        move_list.append(temp_board.san(move))
        temp_board.push(move)
        evaluation_list.append(str(evaluate.evaluate(temp_board.fen())))
    return move_list, evaluation_list


def set_table_content(move_list, evaluation_list):  # set all the moves into the table
    count = 0
    print(str(move_list) + " " + str(evaluation_list))
    for move, evaluation in zip(move_list, evaluation_list):
        move_item = QTableWidgetItem(str(move))
        tableWidget.setItem(count, 0, move_item)
        eval_item = QTableWidgetItem(evaluation)
        tableWidget.setItem(count, 1, eval_item)
        move_item.setTextAlignment(QtCore.Qt.AlignCenter)
        eval_item.setTextAlignment(QtCore.Qt.AlignCenter)
        count += 1


def create_game(text):
    # Allow the user to enter the PGN notation and convert into game
    pgn = io.StringIO(text)
    game = chess.pgn.read_game(pgn)
    return game



def input_game(text):  # retrieve PGN notation and convert into move list and evaluation list
    global input_move_list, final_evaluation_list, final_move_list, input_text

    while True:
        try:
            input_move_list.append(text)

            input_text = " ".join(map(str, input_move_list))

            game = create_game(input_text)

            print(game)

            board = game.board()
            writefile(board)
            final_move_list, final_evaluation_list = generate_move_and_eval_list(game)

            set_table_content(final_move_list, final_evaluation_list)  # set table content using the move list generated

            # print(str(final_move_list) + " " + str(final_evaluation_list))

            text = "Legal move"
            return text
            break
        except:
            text = "Illegal move"
            return text


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global i, board_widget, tableWidget, board, final_move_list, final_evaluation_list, input_text
        i = 0
        # pgn = open("database/lichess_db_standard_rated_2013-01.pgn")
        # game = chess.pgn.read_game(pgn)

        # input_text = "e4 e6"

        game = create_game(input_text)

        board = game.board()
        writefile(board)
        final_move_list, final_evaluation_list = generate_move_and_eval_list(game)

        main_layout = QVBoxLayout()  # set main layout to have a Vertical layout
        top_section = QHBoxLayout()  # set top_section to have a Horizontal layout
        upper_section = QHBoxLayout()  # set upper section to have a Horizontal layout
        lower_section = QHBoxLayout()  # set lower section to have a Horizontal layout

        self.l1 = QLabel("Enter PGN notation:")  # create a label
        self.t1 = QLineEdit()  # create a textbox for user input
        self.b1 = QPushButton("Enter")  # create a button
        self.b1.clicked.connect(self.on_click)  # click button event
        self.l2 = QLabel("")

        top_section.addWidget(self.l1)  # add the widgets to the top section
        top_section.addWidget(self.t1)
        top_section.addWidget(self.b1)
        top_section.addWidget(self.l2)

        tableWidget = QTableWidget()  # initialise table widget
        tableWidget.setRowCount(len(final_move_list))  # set the no of rows for the table
        tableWidget.setColumnCount(2)  # set the no of columns for the table
        tableWidget.setHorizontalHeaderLabels(["Chess Moves", "Evaluation"])  # set column name for the table
        tableWidget.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)  # set table size to fit the content perfectly
        set_table_content(final_move_list, final_evaluation_list)  # set table content using the move list generated
        tableWidget.resizeColumnsToContents()

        board_widget = QtSvg.QSvgWidget('Images/Board.svg')  # initialise board widget
        board_widget.setFixedWidth(460)
        board_widget.setFixedHeight(460)

        upper_section.addWidget(board_widget)  # add the widgets to the upper section
        upper_section.addWidget(tableWidget)

        self.previous_button = QPushButton()  # create a push button for previous move
        self.previous_button.setToolTip("Previous move")
        self.previous_button.setIcon(QtGui.QIcon("Images/left-arrow.png"))
        self.previous_button.clicked.connect(previous_button_clicked)  # create a event handler for the previous button
        self.next_button = QPushButton()  # create a push button for next move
        self.next_button.setToolTip("Next move")
        self.next_button.setIcon(QtGui.QIcon("Images/right-arrow.png"))
        self.next_button.clicked.connect(next_button_clicked)  # create a event handler for the next button

        lower_section.addWidget(self.previous_button)  # add the previous button to the lower section
        lower_section.addWidget(self.next_button)  # add the next button to the lower section

        main_layout.addLayout(top_section)
        main_layout.addLayout(upper_section)  # add the upper section layout to the main_layout
        main_layout.addLayout(lower_section)  # add the lower section layout to the main_layout
        self.setLayout(main_layout)  # set the main layout for the main widget

        self.setWindowTitle("Chess Board")
        self.show()


    @pyqtSlot()
    def on_click(self):
        if not board.is_stalemate() and not board.is_insufficient_material() and not board.is_game_over():
            textboxValue = self.t1.text()
            # QMessageBox.question(self, 'Message', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)

            text = input_game(textboxValue)

            # set_table_content(final_move_list, final_evaluation_list)

            self.l2.setText(text)
            self.t1.setText("")

            # print(str(final_move_list) + " " + str(final_evaluation_list))
            # count = 0
            # for move, evaluation in zip(final_move_list, final_evaluation_list):
            #     move_item = QTableWidgetItem(str(move))
            #     self.tableWidget.setItem(count, 0, move_item)
            #     eval_item = QTableWidgetItem(evaluation)
            #     self.tableWidget.setItem(count, 1, eval_item)
            #     move_item.setTextAlignment(QtCore.Qt.AlignCenter)
            #     eval_item.setTextAlignment(QtCore.Qt.AlignCenter)
            #     count += 1
            #
            # self.tableWidget.update()
        else:
            QMessageBox.question(self, 'Message', "Invalid input", QMessageBox.Ok, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # initialise the pyqt application
    app.setStyleSheet(qdarkstyle.load_stylesheet())  # load third party dark theme
    ex = App()
    sys.exit(app.exec_())
