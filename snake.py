import pygame
from time import sleep
from pygame.locals import *

class Game:
    def __init__(self) -> None:
        pass
    def play(self):
        pass
import random
class Snake:
    #1-up 2-right 3-down 4-left
    def __init__(self) -> None:
        self.dim=(600,400)
        self.color = (200,0,0)
        self.color_br=(255,0,0)
        pygame.init()
        self.canvas=pygame.display.set_mode(self.dim)
        self.fps_clock=pygame.time.Clock()
        self.canvas.fill((0,0,0))
        pygame.display.update()
        pygame.display.set_caption("Snake Game")
        self.fps=10
        self.snake_pos=[]
        self.box_width=15
        self.head=(self.dim[0]//2,self.dim[1]//2)
        # self.snake_pos.append(self.head)
        self.direction=2
        self.score=0
        self.food=None
        self.reset()

    def reset(self) -> None:
        self.head=(self.dim[0]//2,self.dim[1]//2)
        self.snake_pos=[]
        self.snake_pos.append(self.head)
        for i in range(1,3):
            print((self.head[0]+(i*self.box_width),self.head[1]))
            self.snake_pos.append((self.head[0]-(i*self.box_width),self.head[1]))
        print(self.snake_pos)
        self.direction=2
        self.set_food()
        
        
    def draw(self) -> None:
        self.canvas.fill((0,0,0))
        for i in self.snake_pos:        
            pygame.draw.rect(self.canvas,self.color,pygame.Rect(i[0],i[1],self.box_width,self.box_width))
            pygame.draw.rect(self.canvas,self.color_br,pygame.Rect(i[0],i[1],self.box_width,self.box_width),2)
            # print(i,(i[0]+10,i[1]+10))
            # sleep(2)
        pygame.draw.rect(self.canvas,(0,200,0),pygame.Rect(self.food[0],self.food[1],self.box_width,self.box_width),2)

    def move(self):
        
        if self.direction==1:
            self.snake_pos.insert(0,(self.head[0],self.head[1]-self.box_width))
        elif self.direction==2:
            self.snake_pos.insert(0,(self.head[0]+self.box_width,self.head[1]))
        elif self.direction==3:
            self.snake_pos.insert(0,(self.head[0],self.head[1]+self.box_width))
        elif self.direction==4:
            self.snake_pos.insert(0,(self.head[0]-self.box_width,self.head[1]))
        self.head=self.snake_pos[0]
        if self.ate_food():
            pass
        else:
            self.snake_pos.pop()
        return self.check_collision()
    
    def set_food(self):
        self.food=(random.randrange(20,self.dim[0]-20,20),random.randrange(20,self.dim[1]-20,20),)
        while self.food in self.snake_pos:
            self.food=(random.randrange(20,self.dim[0]-20,20),random.randrange(20,self.dim[1]-20,20),)
    
    def check_collision(self) -> bool:
        x,y=self.head
        if x+self.box_width>self.dim[0]:
            return True
        elif x<0:
            return True
        elif self.head in self.snake_pos[1:]:
            return True
        elif y<0:
            return True
        elif y+20>self.dim[1]:
            return True
        else:
            return False
    def ate_food(self) -> bool:
        x,y=self.head
        food_x,food_y=self.food
        if x>=food_x and y>=food_y and x<=food_x+self.box_width and y<=food_y+self.box_width:
            self.score+=1
            print(self.score)
            self.set_food()
            return True
        return False
        
        
        
game=True
pause=True
snake=Snake()
while game:
    snake.fps_clock.tick(snake.fps)
    if pause:
        snake.draw()
    # sleep(1)
        pause=not snake.move()
    # sleep(1)
    else:
        pass
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                snake.direction=1
            elif event.key == K_RIGHT:
                snake.direction=2
            elif event.key == K_DOWN:
                snake.direction=3
            elif event.key == K_LEFT:
                snake.direction=4
            if event.key == K_SPACE:
                pause=not pause            
    