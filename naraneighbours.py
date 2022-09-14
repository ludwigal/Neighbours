import time
import pygame
import numpy as np
import random
COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT= (255, 255, 255)
GREEN = (0, 255, 0)

def update(screen, cells, size , with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    cellcountwhite=0
    cellcountgreen=0
    for row, col in np.ndindex(cells.shape):
        cellcount = ((cells[row - 1:row + 2, col - 1:col + 2])-cells[row,col])
        #print (cellcount)
        if cells[row,col] == 1:
            cellcountwhite = np.count_nonzero(cellcount == 0)-1
            #print(cellcountwhite)
        elif cells[row,col] == 0:
            cellcountwhite = np.count_nonzero(cellcount == 1)
            #print(cellcountwhite)
        if cells[row,col] == 3:
            cellcountgreen = np.count_nonzero(cellcount == 0)-1
            #print(cellcountgreen)
        elif cells[row,col] == 0:
            cellcountgreen = np.count_nonzero(cellcount == 3)
            #print(cellcountgreen)
        #cellcountgreen = np.count_nonzero(cellcount == 2)
        #alivewhite = np.sum(cells[row-1:row+2, col-1:col+2])-cells[row,col]
        #alivegreen = np.sum(cells[row-1:row+2, col-1:col+2])-cells[row,col]
        if cells[row, col] == 0:
            color = COLOR_BG
        elif cells[row,col] == 3:
            color = GREEN
        else:
            color = COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if cellcountwhite <= 2:
                posx = random.randint(0, 599)
                posy = random.randint(0, 799)
                while cells[posx // 10, posy // 10] != 0 and np.count_nonzero(cellcount == 1) < 5:
                    posx = random.randint(0, 599)
                    posy = random.randint(0, 799)
                cells[posx // 10, posy // 10] = 1

                if with_progress:
                    color = COLOR_DIE_NEXT
            #elif 2 <= alive:
             #   updated_cells[row,col] = 1
              #  if with_progress:
               #     color = COLOR_ALIVE_NEXT
            elif cellcountwhite > 2:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        elif cells[row,col] == 0:
            if cellcountwhite > 4:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        if cells[row, col] == 3:
            if cellcountgreen <= 2:
                posx = random.randint(0, 599)
                posy = random.randint(0, 799)
                cells[posx // 10, posy // 10] = 3

                if with_progress:
                    color = COLOR_DIE_NEXT
            #elif 2 <= alive:
             #   updated_cells[row,col] = 1
              #  if with_progress:
               #     color = COLOR_ALIVE_NEXT
            elif cellcountgreen > 2:
                updated_cells[row, col] = 3
                if with_progress:
                    color = GREEN
        elif cells[row,col] == 0:
            if cellcountgreen > 4:
                updated_cells[row, col] = 3
                if with_progress:
                    color = GREEN
        #print(a)
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    #print(np.randint(3, 2))
    cells = np.zeros((60,80))
    #print(cells[0,60])
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)
    for i in range(1000):
        posx = random.randint(0,599)
        posy = random.randint(0,799)
        cells[posx // 10, posy // 10] = 1
    for i in range(1000):
        posx = random.randint(0,599)
        posy = random.randint(0,799)
        cells[posx // 10, posy // 10] = 3
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
                cells[pos[0] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
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
