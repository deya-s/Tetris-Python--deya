import sys
from Figure import Figure
from _collections import defaultdict
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Board(QWidget):

    # keep track of the buttons/ fields
    chain, chain_buttons, chain_dict, chain_outlines = [], defaultdict(tuple), defaultdict(list), defaultdict(tuple)
    fields = [['' for _ in range(7)] for _ in range(14)]
    buttons = defaultdict(tuple)
    #original_fields = [['' for _ in range(7)] for _ in range(14)]
    position = None
    layout = QGridLayout()


    def __init__(self, parent=None):
        super(Board, self).__init__(parent)
        self.resize(400, 400)
        self.setWindowTitle("Tetris")

        # labels
        title = QLabel(self)
        title.setText("This is my tetris board")
        self.error = QLabel(self)
        self.error.setText("")

        self.label_timer = QLabel(self)
        self.label_timer.setText("Timer")

        # creating start button
        self.start_button = QPushButton("Start")

        # making fields as buttons - layout
        self.setLayout(self.layout)

        self.layout.addWidget(title, 0, 0)
        self.layout.addWidget(self.error, 200, 0)
        self.layout.addWidget(self.label_timer, 200, 0)
        self.layout.addWidget(self.start_button, 180, 0)

        self.outlines()
        #print(self.fields)
        # field 0 0 is occupied
        self.fields[0][0].setStyleSheet("background-color: brown;")

        self.original_fields = self.fields

        self.prepareFigure(Figure())

        self.timerComponents()


    def prepareFigure(self, figure):
        self.chain.clear()
        self.chain_dict.clear()
        self.chain_buttons.clear()
        self.chain_outlines.clear()
        self.showFigure(figure.new_figure)
        startIndexX = self.chain[0][0]
        startIndexY = self.chain[0][1]
        for i in range(len(self.chain)):
            self.chain[i] = (self.chain[i][0] - startIndexX, self.chain[i][1] - startIndexY)
            self.chain_dict[self.chain[i][0]] += [self.chain[i][1]]

        startIndex = 0
        for v in list(self.chain_dict.values())[::-1]:
            self.chain_outlines[startIndex] = v
            startIndex -= 1

        print(self.chain_outlines)

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
                    button.show()
                    button.setStyleSheet("background-color: yellow;")
                    self.layout.addWidget(button, 12+x, y)
                    self.chain_buttons[button] = (x, y)
                    self.chain.append((x, y))

        print("Figure shown! :) ")

    def setUpButton(self, button):
        button.setEnabled(True)
        button.clicked.connect(lambda: self.draw_chain(button))

    def dfs(self, i, j, fig, color, text):
        if not self.isValid(i, j, fig) or fig[i][j].text() == '' or fig[i][j].text() == '-':
            return
        fig[i][j].setStyleSheet(color)
        fig[i][j].setText(text)
        self.dfs(i+1, j, fig, color, text)
        self.dfs(i-1, j, fig, color, text)
        self.dfs(i, j+1, fig, color, text)
        self.dfs(i, j-1, fig, color, text)

    def draw_chain(self, button):
        button_x, button_y = self.buttons[button]
        if button.text() != '.':
            if self.position != None:
                position_x, position_y = self.buttons[self.position]
                #print("There was position yes")
                #print(position_x)
                #print(position_y)
                self.dfs(position_x, position_y, self.fields, "background-color: black", '')
            print("Button pressed. ")
            # drawingProceed = True
            for i, els in self.chain_outlines.items():
                for j in els:
                    #print(button_x+i)
                    #print(button_y + j)
                    #print(self.fields[button_x + i][button_y + j].text())
                    if not self.isValid(button_x+i, button_y+j, self.fields) or self.fields[button_x+i][button_y+j].text() == '.' or self.fields[button_x+i][button_y+j].text() == '-':
                        print("Not a good place for the figure ")
                        self.dfs(button_x, button_y, self.fields, "background-color: black", '')
                        return
                    self.fields[button_x+i][button_y+j].setText('..')
                    self.fields[button_x+i][button_y+j].setStyleSheet("background-color: yellow")
            self.fields[button_x][button_y].setText('.')
            self.position = button
            print("Changed :]")
        else:
            print("Button unchecked")
            self.dfs(button_x, button_y, self.fields, "background-color: black", '')

    def outlines(self):
        startBoard = 45

        i_x = 0
        for x in range(startBoard, startBoard+14):
            i_y = 0
            for y in range(startBoard, startBoard+7):
                button = QPushButton('')
                button.show()
                if x == startBoard or y == startBoard or y == startBoard+6 or x == startBoard+13:
                    button.setText('-')
                    button.setStyleSheet("background-color: grey;")
                else:
                    button.setText('')
                    button.setStyleSheet("background-color: black;")
                    self.setUpButton(button)
                self.fields[i_x][i_y] = button
                self.buttons[button] = (i_x, i_y)
                self.layout.addWidget(button, x, y)
                i_y+=1
            i_x+=1

    def start_action(self):
        # making flag true
        self.start = True

        # count = 0
        if self.count == 0:
            self.start = False

        self.count = 50

    def showTimer(self):
        # checking if flag is true
        if self.start:
            # incrementing the counter
            self.count -= 1

            # timer is completed
            if self.count == 0:
                # making flag false

                self.start = False

                self.count = 50

                pos_x, pos_y = self.buttons[self.position]
                self.dfs(pos_x, pos_y, self.fields, "background-color: yellow", '-')
                for b in self.chain_buttons.keys():
                    b.hide()
                self.prepareFigure(Figure())
                # setting text to the label
                self.label_timer.setText("Completed.")

        if self.start:
            # getting text from count
            text = str(self.count / 10) + " s"

            # showing text
            self.label_timer.setText(text)


    def timerComponents(self):
        # count variable
        self.count = 0

        # start flag
        self.start = False

        # setting border to the label
        self.label_timer.setStyleSheet("border : 3px solid black")

        # adding action to the button
        self.start_button.clicked.connect(self.start_action)

        # creating a timer object
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.showTimer)

        # update the timer every tenth second
        timer.start(100)

application = QApplication(sys.argv)
board = Board()
board.show()
sys.exit(application.exec_())
