import random, sys
import pygame
import pygame_textinput

screen = pygame.display.set_mode((750,850), 0, 32)
screen.fill((255,255,255))


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
                    block_color = (238,233,233)

                if self.grid[h][w] == "S":    
                    block_color = (255,0,0)

                if self.grid[h][w] == "E":    
                    block_color = (0,255,0)

                pygame.draw.rect(screen, block_color, (x,y,block_wid,block_hei))

def draw_grid():
    for x in range(0, 750, 15):
        pygame.draw.line(screen, (0,0,0), (x, 100), (x, 850))
    for y in range(100, 850, 15):
        pygame.draw.line(screen, (0,0,0), (0, y), (750, y))

def main():
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
                done = 1
                text = font.render('Enter the ending coordinates(0 < x,y < 50):', True, (0,0,0), (255,255,255))
                #print(coordinates)

            elif done == 1:
                coordinates = string.split(",")
                mygrid.grid[int(coordinates[0])][int(coordinates[1])] = "E"
                done+=1
                #print(coordinates)

            textinput = pygame_textinput.TextInput()
            screen.blit(textinput.get_surface(), (10, 10))
            

        for event in events:
            if pygame.mouse.get_pressed()[0]:
                # print(pygame.mouse.get_pos())
                x_block = (pygame.mouse.get_pos()[0])//15
                y_block = (pygame.mouse.get_pos()[1] - 100)//15
                if(pygame.mouse.get_pos()[1] > 100):
                    mygrid.grid[y_block][x_block] = 1

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        
        mygrid.show(screen)
        draw_grid()
        pygame.display.update()        

        


main()








