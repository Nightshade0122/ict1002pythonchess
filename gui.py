import chess.pgn
import chess.svg
import sys
from PyQt5 import QtSvg, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView


def writefile(board):
    boardsvg = chess.svg.board(board=board)
    f = open("Images/Board.svg", "w")
    f.write(boardsvg)
    f.close()


def next_button_clicked(event):
    global i
    if i < len(move_list):
        board.push(move_list[i])
        writefile(board)
        i += 1
        board_widget.load("Images/board.svg")
    else:
        pass


def previous_button_clicked(event):
    global i
    if i > 0:
        i -= 1
        board.pop()
        writefile(board)
        board_widget.load("Images/board.svg")
    else:
        pass


def generate_move_list(game):
    move_list = []
    for move in game.mainline_moves():
        move_list.append(move)
    return move_list


def set_table_content(move_list):
    count = 0
    for move in move_list:
        tableWidget.setItem(count, 0, QTableWidgetItem("Move.from_uci(" + str(move) + ")"))
        count += 1


if __name__ == '__main__':
    global i
    i = 0
    pgn = open("lichess_db_standard_rated_2013-01.pgn")
    game = chess.pgn.read_game(pgn)
    board = game.board()
    writefile(board)
    move_list = generate_move_list(game)

    app = QApplication(sys.argv)

    main_layout = QVBoxLayout()
    upper_section = QHBoxLayout()
    lower_section = QHBoxLayout()

    window = QWidget()
    tableWidget = QTableWidget()
    tableWidget.setRowCount(len(move_list))
    tableWidget.setColumnCount(1)
    tableWidget.setHorizontalHeaderLabels(["Chess Moves"])
    header = tableWidget.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
    set_table_content(move_list)
    board_widget = QtSvg.QSvgWidget('Images/Board.svg')

    upper_section.addWidget(board_widget)
    upper_section.addWidget(tableWidget)

    previous_button = QPushButton()
    previous_button.setToolTip("Previous move")
    previous_button.setIcon(QtGui.QIcon("Images/left-arrow.png"))
    previous_button.clicked.connect(previous_button_clicked)
    next_button = QPushButton()
    next_button.setToolTip("Next move")
    next_button.setIcon(QtGui.QIcon("Images/right-arrow.png"))
    next_button.clicked.connect(next_button_clicked)

    lower_section.addWidget(previous_button)
    lower_section.addWidget(next_button)

    main_layout.addLayout(upper_section)
    main_layout.addLayout(lower_section)
    window.setLayout(main_layout)
    window.setWindowTitle("Chess Board")
    window.show()
    sys.exit(app.exec_())


