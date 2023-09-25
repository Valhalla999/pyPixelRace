import math
import os
import random
import pygame
from pygame.locals import *
from os import listdir
from os.path import isfile, join
#check if github is working
#i hope now its working

pygame.init()

pygame.display.set_caption("First Race")    #set game name

#Main Variables
size    = width, heigth = (1024, 768)
speed = 3
FPS = 60

window = pygame.display.set_mode((size)) #set window size

#sprites variable
road_w  = int(width/2) 
#car Height and Width
car_w   = int(width/6)
car_h   = int(heigth/4)
#lanes
right_lane = width/2 + road_w/4
left_lane = width/2 - road_w/4
#grass
grass_right = width - road_w/4
grass_left =  road_w/4

#assets
apple_w = int(width/12)
apple_h = int(heigth/12)
#car Names
car1_name = "GreenCar.png"
car2_name = "RedCar.png"

#Random Assest
assets = ["Bush1.png", "TreeBig.png", "Flag.png"]
asset1_ran= random.choice(assets)
fpsClock = pygame.time.Clock()

#Car offset
#window.fill((30, 180, 15))                    #fill background color
roadmark_w = int(width/80)
pygame.display.update() 
font = pygame.font.SysFont("Arial", 32) 


#draw first Car
car = pygame.image.load(join("Cars",car1_name))
car = pygame.transform.scale(car,(car_w,car_h))
car_loc = car.get_rect()
car_loc.center = right_lane, heigth*0.8
car_mask = pygame.mask.from_surface(car)

#draw second car
car2 = pygame.image.load(join("Cars",car2_name))
car2 = pygame.transform.scale(car2,(car_w,car_h))
car2_loc = car2.get_rect()
car2_loc.center = left_lane, heigth*0.2
car2_mask = pygame.mask.from_surface(car2)

#draw assets
asset1 = pygame.image.load(join("assets",asset1_ran))
asset1 = pygame.transform.scale(asset1,(car_w,car_h))
asset1_loc = asset1.get_rect()
asset1_loc.center = grass_left, heigth*0.2
asset1_mask = pygame.mask.from_surface(asset1) 


counter = 0
crash_counter = 0

clock = pygame.time.Clock()
running = True
crash = False

while running:
    clock.tick(FPS)
    
    
    #level
    counter += 1
    if counter == 5000:
        speed +=2
        counter = 0
        print("Level Up", speed)
    
    #spawn new car
    car2_loc[1] += speed
    if car2_loc[1] > heigth:
        crash = False
        if random.randint(0,1) == 0:
            car2_loc.center = right_lane, -200
        else:
            car2_loc.center = left_lane, -200

   
    #spawn a asset1
    asset1_loc[1] += speed
    if asset1_loc[1] > heigth:
        if random.randint(0,1) == 0:
            asset1_loc.center = grass_right , random.randint(-150, -100)
        else:
            asset1_loc.center = grass_left , random.randint(-150, -100)

    #collision ??
    car_mask = pygame.mask.from_surface(car)    # The two cars are colliding
    car2_mask = pygame.mask.from_surface(car2)    # The two cars are colliding
    if car_mask.overlap(car2_mask, (car2_loc.x - car_loc.x, car2_loc.y - car_loc.y)):
        if crash == False:
            crash_counter += 1
            crash = True

    # check exit Quit
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            break

        #key press    
        if event.type == KEYDOWN:
            if event.key in [K_a,K_LEFT]:
                if car_loc.centerx ==  left_lane:
                    print("Max Left Side")
                else:
                    car_loc = car_loc.move([-int(road_w / 2),0])

            if event.key in [K_d,K_RIGHT]:
                if car_loc.centerx == right_lane:
                    print("Max Right Side")
                else:
                    car_loc = car_loc.move([int(road_w / 2),0])

    #draw for gray street
    pygame.draw.rect(
        window,
        (50, 50, 50),
        (width/2-road_w/2, 0, road_w, heigth ))

    #draw for yellow markings
    pygame.draw.rect(
        window,
        (255, 240, 60),
        (width/2 - roadmark_w/2, 0, roadmark_w, heigth ))

    #draw left boarder marking
    pygame.draw.rect(
        window,
        (255, 255, 255),
        (width/2 - road_w/2 + roadmark_w*2, 0, roadmark_w, heigth ))
    #draw right boarder marking
    pygame.draw.rect(
        window,
        (255, 255, 255),
        (width/2 + road_w/2 - roadmark_w * 3 , 0, roadmark_w, heigth ))
    
    #draw grass left side
    pygame.draw.rect(
        window,
        (30, 180, 15),
        (0, 0, width/4, heigth))
    
    #draw grass right side
    pygame.draw.rect(
        window,
        (30, 180, 15),
        (width/2 + road_w/2, 0, width, heigth))

     

    # render the score variable as a surface with some color and background
    counter_lbl = font.render(str(counter), True, (0, 0, 0), (255, 255, 255))
    speed_surface = font.render(str(speed), True, (0, 0, 0), (255, 255, 255))
    crash_lbl = font.render(str(crash_counter), True, (0, 0, 0), (255, 255, 255))

    speed_rect = speed_surface.get_rect()
    speed_rect.topleft = (0, 0)

    counter_rect = counter_lbl.get_rect()
    counter_rect.topleft = (0, 150)

    crash_rect = crash_lbl.get_rect()
    crash_rect.topleft = (0, 300)
       
   
    window.blit(crash_lbl,crash_rect)
    window.blit(speed_surface, speed_rect)
    window.blit(counter_lbl, counter_rect)
    window.blit(car, car_loc)
    window.blit(car2, car2_loc)
    window.blit(asset1, asset1_loc)
    pygame.display.update()
            
pygame.quit