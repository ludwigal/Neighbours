import time
import pygame
import numpy as np
import random
COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
RED= (255, 0, 0)
BLUE = (0, 0, 255)

class Current:
    def __init__(self):
        self.color = 0
        self.with_progress = bool
        self.cells = np.zeros((60,80))
        self.updated_cells = np.zeros((self.cells.shape[0], self.cells.shape[1]))
current=Current()

class CountActor:
    def __init__(self):
        self.countblue = 0
        self.countred = 0

actor=CountActor()



def counting(row,col,cellcount):
    if current.cells[row, col] == 1:
        actor.countred = np.count_nonzero(cellcount == 0) - 1
        actor.countblue = np.count_nonzero(cellcount == 2)

    elif current.cells[row, col] == 0:
        actor.countred = np.count_nonzero(cellcount == 1)

    if current.cells[row, col] == 3:
        actor.countblue = np.count_nonzero(cellcount == 0) - 1
        actor.countred = np.count_nonzero(cellcount == 2)

    elif current.cells[row, col] == 0:
        actor.countblue = np.count_nonzero(cellcount == 3)

def firstcoloractor(row,col):
    if current.cells[row, col] == 0:
        current.color = COLOR_BG
    elif current.cells[row, col] == 3:
        current.color = BLUE
    else:
        current.color = RED

def randomred(row,col,cellcount):
    if current.cells[row, col] == 1:
        if actor.countred <= 2:
            posx = random.randint(0, 599)
            posy = random.randint(0, 799)
            while current.cells[posx // 10, posy // 10] != 0 and np.count_nonzero(cellcount == 1) - 1 < 4:
                posx = random.randint(0, 599)
                posy = random.randint(0, 799)
            current.cells[posx // 10, posy // 10] = 1
            if current.with_progress:
                current.color = COLOR_DIE_NEXT

        elif actor.countred > 2:
            current.updated_cells[row, col] = 1
            if current.with_progress:
                current.color = RED


def randomblue(row,col,cellcount):
    if current.cells[row, col] == 3:
        if actor.countblue <= 2:
            posx = random.randint(0, 599)
            posy = random.randint(0, 799)
            while current.cells[posx // 10, posy // 10] != 0 and np.count_nonzero(cellcount == 3) - 1 < 4:
                posx = random.randint(0, 599)
                posy = random.randint(0, 799)
            current.cells[posx // 10, posy // 10] = 3

            if current.with_progress:
                current.color = COLOR_DIE_NEXT

        elif actor.countblue > 2:
            current.updated_cells[row, col] = 3
            if current.with_progress:
                current.color = BLUE


def updatezeros(row,col):
    if current.cells[row, col] == 0:
        if actor.countblue > 4 and actor.countblue > actor.countred:
            current.updated_cells[row, col] = 3
            if current.with_progress:
                current.color = BLUE
        elif actor.countred > 4 and actor.countred > actor.countblue:
            current.updated_cells[row, col] = 1
            if current.with_progress:
                current.color = RED


#def altutkast():
    # if cells[row, col] == 3:
    #   if cellcountwhite > 5:
    #      cells[row,col] = 1
    # elif cells[row,col] == 1:
    #   if cellcountgreen > 5:
    #      cells[row,col] = 3

def update(screen, cells, size):
    current.with_progress=False
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    for row, col in np.ndindex(cells.shape):
        cellcount = ((cells[row - 1:row + 2, col - 1:col + 2])-cells[row,col])

        counting(row,col,cellcount)

        firstcoloractor(row,col)

        randomred(row,col,cellcount)

        randomblue(row,col,cellcount)

        updatezeros(row,col)

        pygame.draw.rect(screen, current.color, (col * size, row * size, size - 1, size - 1))

    return updated_cells

def main():
    pygame.init()

    screen = pygame.display.set_mode((800,600))

    cells = np.zeros((60,80))

    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    for i in range(400):
        posx = random.randint(0,599)
        posy = random.randint(0,799)
        current.cells[posx // 10, posy // 10] = 1

    for i in range(400):
        posx = random.randint(0,599)
        posy = random.randint(0,799)
        current.cells[posx // 10, posy // 10] = 3

    update(screen, cells, 10)
    pygame.display.update()
    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                        running = not running
                        update(screen, cells, 10)
                        pygame.display.update()
                elif event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    running=False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                current.cells[pos[0] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            current.with_progress=True
            cells = update(screen, cells, 10)
            pygame.display.update()

        time.sleep(0.05)








if __name__ == '__main__':
    main()

#for cells[pos] == 1:
 #   if sum < 3:
  #      posytemp=randokm
   #     posxtemp=random
    #    if cells[posxtemp,posytemp] == 1:
     #       return 1
      #  else: cells[posx,posy] == 0 and cells[posxtemp,posytemp == 1]
