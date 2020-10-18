import chess.pgn
import time
from chessboard import display
from PyQt5 import QtGui, QtSvg, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

def GUI(game):                              #Opens the GUI to run the game
        for move in game.mainline_moves():
                board.push(move)
                time.sleep(1)
                boardsvg = chess.svg.board(board=board)
                f = open("Board.svg", "w")
                f.write(boardsvg)
                f.close()
        app = QtWidgets.QApplication(sys.argv)
        window = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QtSvg.QSvgWidget('Board.svg'))
        layout.addWidget(QPushButton('Top'))
        layout.addWidget(QPushButton('Bottom'))
        window.setLayout(layout)
        window.show()
        sys.exit(app.exec_())

    
 
