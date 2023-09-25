import math
import os
import random
import pygame
from pygame.locals import *
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Pixie Racer")

#Main Variables
size = width, height = (1024,768)
speed = 3
FPS = 30

window = pygame.display.set_mode((size))

#sprites Variables
road_w = int(width/2)

car_w = int(width/6)
car_h = int(height/4)

#lanes
right_lane = width/2 + road_w/4
left_lane = width/2 - road_w/4

#grass
grass_right = width - road_w/4
grass_left = road_w/4


assets = ["Bush1.png","Flag.png"]
#Test Class

class TestRect:
    def __init__(self, name, clr):
        self.name = name
        self.colour = clr

    def detail(self):
        print(self.name + " my color is " + self.colour)
        
gray =TestRect("hope still working", "Red")


class Background:
    def __init__(self, clr, b_pos_x,b_pos_y,b_w,b_h):
        self.colour = clr
        self.positionx = b_pos_x
        self.positiony = b_pos_y
        self.width = b_w
        self.height =b_h

    def back_drawing(self):
        pygame.draw.rect(
        window,
        (self.colour),
        (self.positionx,self.positiony,self.width, self.height))


class Assets:
    def __init__(self,name,transform):
        self.name = name
        self.center = grass_left, height * 0.2
        self.transform = transform
    
    def asset_draw(self):
        # Load the image from the assets folder
        self.image = pygame.image.load(join("assets",self.name))
        # transform the object
        self.image = pygame.transform.scale(self.image,(self.transform))
        #Get the rect object of the image
        self.loc = self.image.get_rect()
        # Move the rect to the center position
        self.loc.center = self.center
        # Get the mask object of the image
        self.mask = pygame.mask.from_surface(self.image)
        # Draw the image on the screen
        window.blit(self.image, self.loc)


    def asset_movement(self):
        self.loc [1] += speed
        if self.loc[1] > height:
            if random.randint(0,1) == 0:
                self.loc.center = grass_right , random.randint(-150, -100)
            else:
                self.loc.center = grass_left , random.randint(-150, -100)
        window.blit(self.image, self.loc)






tree = Assets ("Bush1.png",(car_w,car_h))
flag = Assets ("Flag.png",(car_w,car_h))

green_back =Background((255,255,255),width/2-road_w/2,0,road_w,height )

tree.asset_draw()
flag.asset_draw()


run = True
clock = pygame.time.Clock()
while run:
    

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            break 

    
    flag.asset_movement()
    tree.asset_movement()


    gray.detail()
    green_back.back_drawing()


    pygame.display.update()

    
pygame.quit
