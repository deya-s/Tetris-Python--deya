import sys
from _collections import defaultdict
from Figure import Figure
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Board(QWidget):

    # keep track of the buttons/ fields
    fields = [['' for _ in range(7)] for _ in range(14)]
    buttons = defaultdict(tuple)
    #original_fields = [['' for _ in range(7)] for _ in range(14)]
    position = None
    layout = QGridLayout()
    chain = []
    chain_outlines = defaultdict(list)


    def __init__(self, parent=None):
        super(Board, self).__init__(parent)
        self.resize(400, 400)
        self.setWindowTitle("Tetris")


        # labels
        title = QLabel(self)
        title.setText("This is my tetris board")
        self.error = QLabel(self)
        self.error.setText("")

        # making fields as buttons - layout
        self.setLayout(self.layout)

        self.layout.addWidget(title, 0, 0)
        self.layout.addWidget(self.error, 200, 0)


        self.start()
        self.outlines()
        print(self.fields)
        # field 0 0 is occupied
        self.fields[0][0].setStyleSheet("background-color: brown;")

        self.original_fields = self.fields
        self.dummy_fields = self.fields[:]

        figure1 = Figure()
        print(figure1.new_figure)
        self.showFigure(figure1.new_figure)

        chain_dict = defaultdict(list)
        startIndexX = self.chain[0][0]
        startIndexY = self.chain[0][1]
        for i in range(len(self.chain)):
            self.chain[i] = (self.chain[i][0]-startIndexX, self.chain[i][1]-startIndexY)
            chain_dict[self.chain[i][0]] += [self.chain[i][1]]

        startIndex = 0
        for v in list(chain_dict.values())[::-1]:
            self.chain_outlines[startIndex] = v
            startIndex-=1



    def start(self):
        print("Board ready!! ")

    def isValid(self, x, y, fig):
        if x < 0 or x >= len(fig) or y < 0 or y >= len(fig[0]):
            return False
        return True

    def showFigure(self, fig):
        N, M = len(fig), len(fig[0])
        for x in range(N):
            for y in range(M):
                button = QPushButton("")

                if fig[x][y] == 'x':
                    button.setStyleSheet("background-color: yellow;")
                    self.layout.addWidget(button, 12+x, y)
                    self.chain.append((x, y))

        print("Figure showed! :) ")

    def setUpButton(self, button):
        button.setEnabled(True)
        button.clicked.connect(lambda: self.draw_chain(button))

    def dfs(self, i, j, fig ):
        if not self.isValid(i, j, fig) or fig[i][j].text() == '' or fig[i][j].text() == '-':
            return
        fig[i][j].setStyleSheet("background-color: black")
        fig[i][j].setText('')
        self.dfs(i+1, j, fig)
        self.dfs(i-1, j, fig)
        self.dfs(i, j+1, fig)
        self.dfs(i, j-1, fig)

    def draw_chain(self, button):
        button_x, button_y = self.buttons[button]
        if button.text() != '.':
            if self.position != None:
                position_x, position_y = self.buttons[self.position]
                print("There was position yes")
                print(position_x)
                print(position_y)
                self.dfs(position_x, position_y, self.fields)
            print("Button pressed. ")
            drawingPossible = True
            for i, els in self.chain_outlines.items():
                if not drawingPossible:
                    self.dfs(button_x, button_y, self.fields)
                    break
                for j in els:
                    print(button_x+i)
                    print(button_y + j)
                    print(self.fields[button_x + i][button_y + j].text())
                    if not self.isValid(button_x+i, button_y+j, self.fields) or self.fields[button_x+i][button_y+j].text() == '.'or self.fields[button_x+i][button_y+j].text() == '-':
                        print("Not a good place for the figure ")
                        self.dummy_fields = self.fields[:]
                        drawingPossible = False
                        break
                    self.dummy_fields[button_x+i][button_y+j].setText('..')
                    self.dummy_fields[button_x+i][button_y+j].setStyleSheet("background-color: yellow")
            self.fields = self.dummy_fields
            #self.dummy_fields = self.original_fields[:]
            self.fields[button_x][button_y].setText('.')
            self.position = button
            print("Changed :]")
        else:
            print("Button unchecked")
            self.dfs(button_x, button_y, self.fields)

    def outlines(self):
        startBoard = 45

        i_x = 0
        for x in range(startBoard, startBoard+14):
            i_y = 0
            for y in range(startBoard, startBoard+7):
                button = QPushButton("")
                if x == startBoard or y == startBoard or y == startBoard+6 or x == startBoard+13:
                    button.setText('-')
                    button.setStyleSheet("background-color: grey;")
                else:
                    button.setStyleSheet("background-color: black;")
                self.setUpButton(button)
                self.fields[i_x][i_y] = button
                self.buttons[button] = (i_x, i_y)
                self.layout.addWidget(button, x, y)
                i_y+=1
            i_x+=1


application = QApplication(sys.argv)
board = Board()
board.show()
sys.exit(application.exec_())