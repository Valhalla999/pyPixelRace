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
size = width, height = (1024, 768)
speed = 3
FPS = 60
Player_car = "GreenCar.png"
crash = False

#Colours
grass_green = (30,180,15)
street_gray = (50,50,50)
boarder_white = (255,255,255)

window = pygame.display.set_mode((size))

#sprites Variables
road_w = int(width/2)
roadmark_w = int(width/80)
car_w = int(width/6)
car_h = int(height/4)
bush_w =int(100)
bush_h = int(100)

#lanes
right_lane = width/2 + road_w/4
left_lane = width/2 - road_w/4

#grass
grass_right = int(width - road_w/4)
grass_left = int(road_w/4)

#Create the assets list
asset_list = []


class Player:
    def __init__(self, name, draw_offset, transform):
        self.name = name
        self.center = right_lane, draw_offset
        self.transform = transform
    
    def player_draw(self):
        # Load the image from the assets folder
        self.image = pygame.image.load(join("Cars",self.name))
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

    def player_movement(self):
        if event.type == KEYDOWN:
            if event.key in [K_a, K_LEFT]:
                if self.loc.centerx ==  left_lane:
                    pass
                else:
                    self.loc = self.loc.move([-int(road_w / 2),0])

            if event.key in [K_d, K_RIGHT]:
                if self.loc.centerx == right_lane:
                    pass
                else:
                    self.loc = self.loc.move([int(road_w / 2),0])
        window.blit(self.image, self.loc)                 


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
        self.image = pygame.image.load(join("assets",self.name)).convert_alpha()
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


def asset_collision(asset_list):
    for i in range(len(asset_list)):
        for j in range(i+1, len(asset_list)):
            if asset_list[i].mask.overlap(asset_list[j].mask, (asset_list[j].loc.x - asset_list[i].loc.x, asset_list[j].loc.y - asset_list[i].loc.y)):
                asset_list[i].loc[1] -= random.randint (10,450) 
                #Crash sound
        else:
            pass


class middle_line:
    def __init__(self,name,transform, draw_offset):
        self.name = name
        self.center = width/2, draw_offset
        self.transform = transform
    
    def middle_line_draw(self):
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

    def middle_line_move(self):
        self.loc [1] += speed
        if self.loc[1] > height:            
            self.loc.center = width/2, -50
        window.blit(self.image, self.loc)


class Labels:
    def __init__(self, text, size, colour, position):
        self.text = text
        self.size = size
        self.colour = colour
        self.position = position

    def label_draw(self):
        self.font = pygame.font.SysFont("Arial", self.size)
        self.text = self.font.render(self.text, True, self.colour)
        self.textRect = self.text.get_rect()
        self.textRect.center = self.position
        window.blit(self.text, self.textRect)



class enemie:
    def __init__(self,name,transform, draw_offset,crash):
        self.name = name
        if random.randint(0,1) == 0:
            self.center = left_lane, draw_offset
        else:
            self.center = right_lane, draw_offset
        self.transform = transform
        self.crash = crash
    
    def enemie_draw(self):
        # Load the image from the assets folder
        self.image = pygame.image.load(join("enemies",self.name)).convert_alpha()
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

    def enemie_movement(self):
        self.loc [1] += speed
        if self.loc[1] > height: 
            global crash
            crash = False          
            if random.randint(0,1) == 0:
                self.loc.center = right_lane, random.randint (-150, -10)
            else:
                self.loc.center = left_lane, random.randint (-150, -10)
        window.blit(self.image, self.loc)


#defining the offset
asset_main_offset = 0


#defining the Assets

bush_amount = 0
bushes = []

while bush_amount < 10:
    bush_name = "bush" + str(bush_amount + 1)
    bushes.append(Assets("Bush1.png", (bush_w, bush_h), asset_main_offset))
    asset_list.append(bushes[bush_amount])
    bush_amount += 1

#defining treeBig assets
tree_amount = 0
trees = []
while tree_amount < 4:
   tree_name = "tree" + str(tree_amount + 1)
   trees.append(Assets("TreeBig.png", (car_w,car_h), asset_main_offset))
   asset_list.append(trees[tree_amount])
   tree_amount += 1


#define and draw player
player1 = Player(Player_car, height -100, (car_w,car_h))
player1.player_draw()

#define enemie
enemiecar1 = enemie("RedCar.png", (car_w,car_h), -200, crash)
enemiecar1.enemie_draw()

#random draw the assets
for i in range(len(asset_list)):
    asset_list[i].asset_draw()

#define the Background     
grass_background = Background((grass_green),0,0,width,height)
street_background =Background((street_gray),width/2-road_w/2,0,road_w,height )
right_boardermarking = Background((boarder_white), width/2 + road_w/2 - roadmark_w * 3, 0, roadmark_w, height )
left_boardermarking = Background((boarder_white), width/2 - road_w/2 + roadmark_w * 2, 0, roadmark_w, height)



#middle line
middle = middle_line("Flag.png", (car_w, car_h), -50)
middle.middle_line_draw()

counter = 0 
run = True
clock = pygame.time.Clock()


while run:
    
    counter += 1
    if counter == 150:
        speed +=1
        counter = 0
        print("Level Up", speed)
    
    #Base Data
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            break 
    
    #Collision Player/Enemiecar
    if player1.mask.overlap(enemiecar1.mask, (enemiecar1.loc.x  - player1.loc.x , enemiecar1.loc.y - player1.loc.y)):
        if crash == False:
            print("Crash")
            crash = True
    
            
    # Background drawing
    grass_background.back_drawing()
    street_background.back_drawing()
    right_boardermarking.back_drawing()
    left_boardermarking.back_drawing()

    middle.middle_line_move()

   
    #assets movement
    for i in range(len(asset_list)):
        asset_list[i].asset_movement()
    
    #enemie movement
    enemiecar1.enemie_movement()

    #Player movement
    player1.player_movement()
    
    

    asset_collision(asset_list)

    #labels
    speed_lbl = Labels(str(speed), 20, (255,255,255), (width/2, 20))
    counter_lbl = Labels(str(counter), 20, (255,255,255), (width/2, 50))


    speed_lbl.label_draw()
    counter_lbl.label_draw()

    
    pygame.display.update()
    
pygame.quit