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
roadmark_w = int(width/80)
car_w = int(width/6)
car_h = int(height/4)

#lanes
right_lane = width/2 + road_w/4
left_lane = width/2 - road_w/4

#grass
grass_right = int(width - road_w/4)
grass_left = int(road_w/4)


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
    def __init__(self,name,transform, draw_offset):
        self.name = name
        if random.randint(0,1) == 0:
            self.center = grass_left, draw_offset
        else:
            self.center = grass_right, draw_offset

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
                self.loc.center = grass_right, random.randint (-150, -10)
            else:
                self.loc.center = grass_left, random.randint (-150, -10)
        window.blit(self.image, self.loc)



def crash(Assets_list):
    for i in range(len(Assets_list)):
        for j in range(i+1, len(Assets_list)):
            if Asset_list[i].mask.overlap(Asset_list[j].mask, (Asset_list[j].loc.x - Asset_list[i].loc.x, Asset_list[j].loc.y - Asset_list[i].loc.y)):
                Asset_list[i].loc[1] -= 50 
                print("crash", tree.loc.y , tree2.loc.y)
        else:
            pass


#define the offset
tree_offset = 0
tree2_offset = 0
flag_offset = 0

#defining the Assets
flag = Assets ("Flag.png",(car_w,car_h),flag_offset)
tree = Assets ("Bush1.png",(car_w,car_h),tree_offset)
tree2 = Assets ("TreeBig.png",(car_w,car_h),tree2_offset)

#draw the assets
tree.asset_draw()
tree2.asset_draw()
flag.asset_draw()
#collision ??
Asset_list = [tree, tree2, flag]

# tree01 = pygame.mask.from_surface(tree)    # The two cars are colliding
# tree02 = pygame.mask.from_surface(tree2)    # The two cars are colliding



#define the Background
grass_background = Background((30,180,15),0,0,width,height)
street_background =Background((50,50,50),width/2-road_w/2,0,road_w,height )
right_boardermarking = Background((255,255,255), width/2 + road_w/2 - roadmark_w * 3, 0, roadmark_w, height )
left_boardermarking = Background((255,255,255), width/2 - road_w/2 + roadmark_w * 2, 0, roadmark_w, height)


run = True
clock = pygame.time.Clock()

while run:
    

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            break 
    
    grass_background.back_drawing()
    street_background.back_drawing()
    right_boardermarking.back_drawing()
    left_boardermarking.back_drawing()
    tree.asset_movement()
    tree2.asset_movement()
    flag.asset_movement()
    crash(Asset_list)
    
    #print(tree.loc.centery, tree2.loc.centery, flag.loc.centery)

    pygame.display.update()
    
pygame.quit