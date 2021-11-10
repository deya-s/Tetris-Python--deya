from Tetris import Tetris
import random

class Figure(Tetris):
    limitX, limitY = 6, 4
    randomX, randomY = random.randint(1, limitX), random.randint(1, limitY)
    new_figure = None
    def __init__(self):
        self.start()
        self.new_figure = [['' for _ in range(self.randomY)] for _ in range(self.randomX)]

        self.getRandom()



    def start(self):
        print("New figure")

    def isValid(self, x, y):
        if x < 0 or x >= self.randomX or y < 0 or y >= self.randomY:
            return False
        return True

    def getRandom(self):
        capacity = self.randomX*self.randomY
        print(capacity)
        fieldstodraw = random.randint(1, capacity)

        print("New figure outlines and howw many fields")
        print(self.new_figure)
        print(fieldstodraw)

        occupied_places = set()

        randomX_todraw = random.randint(0, self.randomX - 1)
        randomY_todraw = random.randint(0, self.randomY - 1)
        print(randomX_todraw)
        print(randomY_todraw)

        while fieldstodraw > 0:
            up_down_left_right = random.randint(0, 3)
            if up_down_left_right == 0:
                if not self.isValid(randomX_todraw-1, randomY_todraw):
                    continue
                randomX_todraw-=1
            elif up_down_left_right == 1:
                if not self.isValid(randomX_todraw+1, randomY_todraw):
                    continue
                randomX_todraw += 1
            elif up_down_left_right == 2:
                if not self.isValid(randomX_todraw, randomY_todraw-1):
                    continue
                randomY_todraw -= 1
            elif up_down_left_right == 3:
                if not self.isValid(randomX_todraw, randomY_todraw+1):
                    continue
                randomY_todraw += 1

            if (randomX_todraw, randomY_todraw) in occupied_places:
                continue
            else:
                occupied_places.add((randomX_todraw, randomY_todraw))
            self.new_figure[randomX_todraw][randomY_todraw] = 'x'
            fieldstodraw-=1




f1 = Figure()
for el in f1.new_figure:
    print(el)