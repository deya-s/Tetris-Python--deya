import sys
from Figure import Figure
from _collections import defaultdict
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Board(QWidget):
    chain = []
    position = None
    timerParam = 500
    layout = QGridLayout()
    start = False


    def __init__(self, parent=None):
        self.fX, self.fY = 14, 10  # rows, columns
        self.topMiddle = (1, self.fY // 2)  # top middle place for first appearance of figure
        self.fields = [['' for _ in range(self.fY)] for _ in range(self.fX)]
        self.original = [['' for _ in range(self.fY)] for _ in range(self.fX)]
        self.occupied_places = [['' for _ in range(self.fY)] for _ in range(self.fX)]
        # self.highestRow = len(self.fields) - 1
        super(Board, self).__init__(parent)
        self.resize(400, 400)
        self.setWindowTitle("Tetris")
        self.running = True  # making sure that it is not gameover
        # title
        title = QLabel(self)
        title.setText("This is my tetris board")
        # error label for gameover
        self.error = QLabel(self)
        self.error.setText("")

        # start button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(lambda: self.start_game())

        self.score = 0
        self.scoreL = QLabel(self)
        self.scoreL.setStyleSheet("background-color: orange")
        self.scoreL.setText(str(self.score))

        # setting layout
        self.setLayout(self.layout)

        # adding elements to layout
        self.layout.addWidget(title, 0, 0)
        self.layout.addWidget(self.error, 200, 0)
        self.layout.addWidget(self.start_button, 180, 0)
        self.layout.addWidget(self.scoreL, 160, 0)

        # 'drawing' the board
        self.outlines()

        # timer object
        self.timer = QTimer(self)

        # adding action to timer
        self.timer.timeout.connect(self.showTimer)

        # adding action to arrowkeys to move figure
        QShortcut(QKeySequence(Qt.Key_Left), self, activated=self.move_left)
        QShortcut(QKeySequence(Qt.Key_Right), self, activated=self.move_right)
        QShortcut(QKeySequence(Qt.Key_Down), self, activated=self.move_down)



    def rowFull(self):
        fullR = '.' + ('x' * (self.fY-2)) + '.'
        lines = 0
        for i in range(self.fX):
            if ''.join(self.occupied_places[i]) == fullR:
                print("Full row :)")
                cur_fields = self.fX-2
                for x in range(self.fX-2,0,-1):
                    if cur_fields == i:
                        cur_fields-=1
                    for y in range(self.fY-2,0,-1):
                        text = self.fields[cur_fields][y].text()
                        self.fields[x][y].setText(text)
                        color = self.fields[cur_fields][y].palette().window().color().name()
                        self.fields[x][y].setStyleSheet("background-color:" + str(color) + ";")
                        if text == '-':
                            self.occupied_places[x][y] = 'x'
                        else:
                            self.occupied_places[x][y] = ''
                    cur_fields-=1
                    if cur_fields == 0:
                        cur_fields+=1
                lines+=1
        if lines == 1:
            self.score+=40
        elif lines == 2:
            self.score+=100
        elif lines== 3:
            self.score+=300
        elif lines > 3:
            self.score+=1200
        self.scoreL.setText(str(self.score))

    def start_game(self):
        self.prepareFigure(Figure())
        if self.error.text() == "Game over":
            self.error.setText('')
            self.outlines()
            self.running = True
            self.score = 0
            self.scoreL.setText(str(self.score))

    def prepareFigure(self, figure):
        print("Occupied places")
        print(self.occupied_places)
        self.chain.clear()
        self.showFigure(figure.new_figure)
        print("Rows :)")
        self.rowFull()
        if self.running:
            self.start = True
            self.timerMethod()
        else:
            self.start = False

    def isValid(self, x, y, fig):
        if x < 0 or x >= len(fig) or y < 0 or y >= len(fig[0]):
            return False
        return True

    def showFigure(self, fig):
        N, M = len(fig), len(fig[0])
        i, j = self.topMiddle[0], self.topMiddle[1]
        figX, figY = None, None
        for x in range(N):
            for y in range(M):
                if fig[x][y] == 'x':
                    if figX == None and figY == None:
                        figX, figY = x, y
                    #print(self.fields[i + x - figX][j + y - figY])
                    if self.fields[i + x - figX][j + y - figY].text() == '-':
                        #if self.fields[i + x - figX][j + y - figY].text() == '.' or self.fields[i + x - figX][j + y - figY].text() == '-':
                        self.error.setText("Game over")
                        print("Game over")
                        self.running = False
                        break
                    self.fields[i + x - figX][j + y - figY].setText(":)")
                    self.fields[i + x - figX][j + y - figY].setStyleSheet("background-color: green;")
                    self.chain.append([i + x - figX, j + y - figY])

        #print("Figure shown! :) ")


    def dfs(self, i, j, fig, color, text):
        if not self.isValid(i, j, fig) or fig[i][j].text() == '' or fig[i][j].text() == '-':
            return
        fig[i][j].setStyleSheet(color)
        fig[i][j].setText(text)
        self.dfs(i+1, j, fig, color, text)
        self.dfs(i-1, j, fig, color, text)
        self.dfs(i, j+1, fig, color, text)
        self.dfs(i, j-1, fig, color, text)


    def outlines(self):
        startBoard = 45
        self.layout.setSpacing(2)
        i_x = startBoard

        for x in range(self.fX):
            i_y = startBoard
            for y in range(self.fY):
                edge = QLabel('', self)
                edge.show()
                edge.setFixedSize(35,27)
                if x == 0 or x == self.fX - 1 or y == 0 or y == self.fY - 1:
                    edge.setText('.')
                    edge.setStyleSheet("QLabel {border: 3px solid darkgrey; background-color: aliceblue;}")
                    self.occupied_places[x][y] = '.'
                else:
                    edge.setStyleSheet("background-color: black;")
                self.fields[x][y] = edge
                self.layout.addWidget(self.fields[x][y], i_x, i_y)
                i_y += 1
            i_x += 1


    def timerMethod(self):
        self.count = 10
        # update the timer
        self.timer.start(self.timerParam)


    def showTimer(self):
        #self.rowFull()
        # checking if game is started
        if self.start:
            #print("Showwing timer :)")
            self.lowerbounds = []
            lowestRow = self.chain[-1][0]
            for el in self.chain[::-1]:
                if el[0] == lowestRow:
                    self.lowerbounds.append(el[0])
                else:
                    break
            # incrementing the counter
            self.count -= 1
            if self.fX-2 in self.lowerbounds:
                self.start=False
                for el in self.chain:
                    self.fields[el[0]][el[1]].setText('-')
                    self.fields[el[0]][el[1]].setStyleSheet(" QLabel {background-color: aliceblue;}")
                    self.occupied_places[el[0]][el[1]] = "x"
                self.prepareFigure(Figure())
            # getting text from count
            text = str(self.count / 10) + " s"
            for el in self.chain:
                self.fields[el[0]][el[1]].setStyleSheet("background-color: black;")
                self.fields[el[0]][el[1]].setText('')
                el[0] += 1
            for el in self.chain:
                self.fields[el[0]][el[1]].setStyleSheet("background-color: green;")
                self.fields[el[0]][el[1]].setText(':)')
                if self.start and self.isValid(el[0]+1, el[1], self.fields) and self.fields[el[0]+1][el[1]].text() == '-':
                    self.start = False
                    for el in self.chain:
                        self.fields[el[0]][el[1]].setText('-')
                        self.fields[el[0]][el[1]].setStyleSheet(" QLabel {background-color: aliceblue;}")
                        self.occupied_places[el[0]][el[1]] = "x"
                    self.prepareFigure(Figure())
            # showing text
            print(text)


    def move_left(self):
        goLeft = True
        for el in self.chain:
            if not self.isValid(el[0], el[1]-1, self.fields) or self.fields[el[0]][el[1]-1].text()=='.' or self.fields[el[0]][el[1]-1].text()=='-':
                print("Cannot go left")
                goLeft = False
        if goLeft:
            for el in self.chain:
                self.fields[el[0]][el[1]].setStyleSheet("background-color: black;")
                self.fields[el[0]][el[1]].setText('')
                el[1] -= 1
            # draw new figure
            for el in self.chain:
                self.fields[el[0]][el[1]].setStyleSheet("background-color: green;")
                self.fields[el[0]][el[1]].setText(':)')


    def move_right(self):
        goRight = True
        for el in self.chain:
            if not self.isValid(el[0], el[1] + 1, self.fields) or self.fields[el[0]][el[1] + 1].text() == '.' or \
                    self.fields[el[0]][el[1] + 1].text() == '-':
                print("Cannot go right")
                goRight = False
        if goRight:
            for el in self.chain:
                self.fields[el[0]][el[1]].setStyleSheet("background-color: black;")
                self.fields[el[0]][el[1]].setText('')
                el[1] += 1
            # draw new figure
            for el in self.chain:
                self.fields[el[0]][el[1]].setStyleSheet("background-color: green;")
                self.fields[el[0]][el[1]].setText(':)')


    def move_down(self):
        goDown = True
        for el in self.chain:
            if not self.isValid(el[0] + 1, el[1], self.fields) or self.fields[el[0] + 1][el[1]].text() == '.' or \
                    self.fields[el[0] + 1][el[1]].text() == '-':
                print("Cannot go down")
                goDown = False
        if goDown:
            for el in self.chain:
                self.fields[el[0]][el[1]].setStyleSheet("background-color: black;")
                self.fields[el[0]][el[1]].setText('')
                el[0] += 1
            # draw new figure
            for el in self.chain:
                self.fields[el[0]][el[1]].setStyleSheet("background-color: green;")
                self.fields[el[0]][el[1]].setText(':)')


application = QApplication(sys.argv)
board = Board()
board.show()
sys.exit(application.exec_())
