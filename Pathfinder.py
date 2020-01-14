import random, sys
import pygame
import pygame_textinput
import numpy as np
import queue

screen = pygame.display.set_mode((750,850), 0, 32)

screen.fill((255,255,255))


m = np.zeros((50,50), dtype=int)

R = 50 #Number of Rows 
C = 50 #Number of Columns

sr = 0 #starting row number
sc = 0 #strating column number
rq = queue.Queue(0) #empty row queue
cq = queue.Queue(0) #empty column queue


reached_end = False
visited = np.zeros((50,50), dtype=int)
parent = np.zeros((50,50), dtype=int)

#hard coded for now
parent[0][0] = 10000

#north, south, east, west direction vectors
dr = [-1, +1, 0, 0] 
dc = [0, 0, +1, -1]

#variables to track number of steps
move_count = 0
nodes_current_layer = 1
nodes_next_layer = 0
column = 0
row = 0


def explore_neighbours(r,c,matrix):
    global nodes_next_layer

    m = matrix
    for i in range(0,4):
        rr = r + dr[i]
        cc = c + dc[i]

        if rr<0 or cc < 0: continue
        if rr >=R or cc >= C: continue

        if visited[rr][cc]: continue
        if m[rr][cc] == 'B': continue

        rq.put(rr)
        cq.put(cc)
        parent[rr][cc] = (r)*C + c
        visited[rr][cc] = 1
        nodes_next_layer += 1




def solver(matrix):
    rq.put(sr)
    cq.put(sc)
    m = matrix
    # for i in range(0,50):
    #     for j in range(0,50):
    #         print(m[i][j], end = " ")
    #     print(" ")

    visited[sr][sc] = 1
    global nodes_current_layer
    global move_count
    global nodes_next_layer
    global row
    global column
    global reached_end

    while rq.qsize() > 0:
        r = rq.get()
        c = cq.get()
        if m[r][c] == 'E':
            row = r 
            column = c
            reached_end = True
            break
        explore_neighbours(r,c,m)
        nodes_current_layer -= 1
        if nodes_current_layer == 0:
            nodes_current_layer = nodes_next_layer
            nodes_next_layer = 0
            move_count += 1
    if reached_end:
        return move_count
    return -1





















class Grid:
    def __init__(self, width, height, num_colors=2):
        self.wid = width
        self.hei = height
        # self.no_colors = num_colors
        # self.color_list = [[None]*num_colors for n in range(num_colors)]
        # self.color_list[0] = (238,233,233)
        # self.color_list[1] = (238,213,183)

        self.grid = [[0 for i in range(width)] for j in range(height)]

    def show(self, screen):
        for h in range(self.hei):
            for w in range(self.wid):
                x = 15*w
                y = 100 + 15*h
                block_hei = 15
                block_wid = 15
                
                if self.grid[h][w] == 0:
                    block_color = (238,213,183)

                if self.grid[h][w] == 1:
                    block_color = (0,0,255)

                if self.grid[h][w] == "B":
                    block_color = (238,233,233)

                if self.grid[h][w] == "S":    
                    block_color = (0,255,0)

                if self.grid[h][w] == "E":    
                    block_color = (255,0,0)

                pygame.draw.rect(screen, block_color, (x,y,block_wid,block_hei))

def draw_grid():
    for x in range(0, 750, 15):
        pygame.draw.line(screen, (0,0,0), (x, 100), (x, 850))
    for y in range(100, 850, 15):
        pygame.draw.line(screen, (0,0,0), (0, y), (750, y))

def main():
    global row
    global column
    global sr
    global sc
    pygame.init()
    done = 0
    mygrid = Grid(50,50)
    mygrid.show(screen)
    textinput = pygame_textinput.TextInput()

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Enter the starting coordinates(0 < x,y < 50):', True, (0,0,0), (255,255,255))
    textRect = text.get_rect()
    textRect.center = (750 // 2, 20)

    while True:
        screen.fill((255,255,255))
        events = pygame.event.get()
        screen.blit(textinput.get_surface(), (750//2, 50))
        screen.blit(text, textRect) 

        if textinput.update(events):
            string = textinput.get_text()
            print(textinput.get_text())

            if done == 0:
                coordinates = string.split(",")
                mygrid.grid[int(coordinates[0])][int(coordinates[1])] = "S"
                sr = int(coordinates[0])
                sc = int(coordinates[1])
                done = 1
                text = font.render('Enter the ending coordinates(0 < x,y < 50):', True, (0,0,0), (255,255,255))
                #print(coordinates)

            elif done == 1:
                coordinates = string.split(",")
                mygrid.grid[int(coordinates[0])][int(coordinates[1])] = "E"
                done+=1
                #print(coordinates)

            elif done == 2:
                output = solver(mygrid.grid)
                #print(row)
                if (output != -1):
                    val = parent[row][column]
                    # print("Parent Matrix: ")
                    # print(parent)
                    # print("Path:")
                    # print(sr)
                    # print(sc)
                    while val != 10000:
                        if row == sr and column == sc: 
                            break
                        #print("(",row,",", column,")")
                        mygrid.grid[row][column] = 1
                        column = val%C
                        row = int((val-column)/C)
                        val = parent[row][column]
                #print ("( 0 , 0 )")


            textinput = pygame_textinput.TextInput()
            screen.blit(textinput.get_surface(), (10, 10))
            

        for event in events:
            if pygame.mouse.get_pressed()[0]:
                # print(pygame.mouse.get_pos())
                x_block = (pygame.mouse.get_pos()[0])//15
                y_block = (pygame.mouse.get_pos()[1] - 100)//15
                if(pygame.mouse.get_pos()[1] > 100):
                    mygrid.grid[y_block][x_block] = "B"

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        
        mygrid.show(screen)
        draw_grid()
        pygame.display.update()        

        


main()








