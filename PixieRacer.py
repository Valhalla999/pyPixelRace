import math
import os
import random
import pygame
from pygame.locals import *
from os import listdir
from os.path import isfile, join
from time import sleep
import button

pygame.init()

pygame.display.set_caption("Pixie Racer")

#Main Variables
size = width, height = (1024,768)
speed = 5 #change also in Menu function
FPS = 60
Player_car = "Green_F1_Car.png"
enemie_car_png = "Blue_F1_Car.png"
crash = False
main_lives = 4 
loot_collision = False
game_paused = True
Level = 0
main_theme_music = "music/MainTheme.wav"
coin_theme_music = "music/CoinPickup.wav"

#Background color
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

#assetsManager
asset_list = []
bushes = []
trees = []
asset_main_offset = 0
bush_amount = 0
tree_amount = 0
bush_max = 8
tree_max = 2
lives_size  = 125,125
lives_location = (width/2, 60)

#ScoreList
score = 0
coin_score = 5
banana_score = 1

#Menu
font = pygame.font.SysFont("Arial", 32)
text_col = (255,255,255)
def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    window.blit(img, (x,y))
resume_img = pygame.image.load("Menu/button_resume.png").convert_alpha()
quit_img = pygame.image.load("Menu/button_quit.png").convert_alpha()


#createButtons


#Music
theme_sound = pygame.mixer.Sound(main_theme_music)
coin_sound =pygame.mixer.Sound(coin_theme_music)
pygame.mixer.set_num_channels(2)



#Classe 
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
            self.center = grass_left, -150
        else:
            self.center = grass_right, -150

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
        if self.loc[1] > height + 100:            
            if random.randint(0,1) == 0:
                self.loc.center = grass_right, random.randint (-250, -100)
            else:
                self.loc.center = grass_left, random.randint (-250, -100)
        window.blit(self.image, self.loc)

def asset_collision(asset_list):
    for i in range(len(asset_list)):
        for j in range(i+1, len(asset_list)):
            if asset_list[i].mask.overlap(asset_list[j].mask, (asset_list[j].loc.x - asset_list[i].loc.x, asset_list[j].loc.y - asset_list[i].loc.y)):
                asset_list[i].loc[1] -= random.randint(10, 300)
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
    def __init__(self,name,transform, draw_offset,crash,rotation):
        self.name = name
        if random.randint(0,1) == 0:
            self.center = left_lane, draw_offset
        else:
            self.center = right_lane, draw_offset
        self.transform = transform
        self.crash = crash
        self.rotation = rotation
    
    def enemie_draw(self):
        # Load the image from the assets folder
        self.image = pygame.image.load(join("enemies",self.name)).convert_alpha()
        # transform the object
        self.image = pygame.transform.scale(self.image,(self.transform))
        #rotate the object
        self.image = pygame.transform.rotate(self.image, self.rotation)
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
                self.loc.center = right_lane, random.randint (-150, -50)
            else:
                self.loc.center = left_lane, random.randint (-150, -50)
        window.blit(self.image, self.loc)

class loot:
    def __init__(self,name,transform, draw_offset,crash,rotation,score):
        self.name = name
        if random.randint(0,1) == 0:
            self.center = left_lane, draw_offset
        else:
            self.center = right_lane, draw_offset
        self.transform = transform
        self.crash = crash
        self.rotation = rotation
        self.score = score
           

    def loot_draw(self):
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

    def loot_movement(self):
        global loot_collision
        loot_collision = False
        if self.mask.overlap(enemiecar1.mask, (enemiecar1.loc.x  - self.loc.x , enemiecar1.loc.y - self.loc.y)):
            self.loc.y -= random.randint(25, 125)
        else:
            pass
        self.loc [1] += speed
        if self.loc[1] > height:                   
            if random.randint(0,1) == 0: 
                self.loc.center = right_lane, random.randint (-150, -10)
            else:
                self.loc.center = left_lane, random.randint (-150, -10)
        window.blit(self.image, self.loc)


    def car_collision(self):
        global score
        global loot_collision
        if self.mask.overlap(player1.mask, (player1.loc.x  - self.loc.x , player1.loc.y - self.loc.y)):
            if loot_collision == False:
                print ("Crash")
                score += self.score
                print("SoundPlay")
                channel2.play(coin_sound)
                loot_collision = True
                self.loc.centery = - 150
            else:
                pass        
        window.blit(self.image, self.loc)
    
class health_bar:
    def __init__(self, name, transform, draw_offset):
        self.name = name
        self.center = draw_offset
        self.transform = transform
    def lives_draw(self):
        self.image = pygame.image.load(join("assets",self.name)).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.transform))
        self.loc = self.image.get_rect()
        self.loc.center = self.center
        window.blit(self.image, self.loc)


#Create the assets list
while bush_amount < bush_max:
    bush_name = "bush" + str(bush_amount + 1)
    bushes.append(Assets("Bush1.png", (bush_w, bush_h), asset_main_offset))
    asset_list.append(bushes[bush_amount])
    bush_amount += 1

while tree_amount < tree_max:
   tree_name = "tree" + str(tree_amount + 1)
   trees.append(Assets("TreeBig.png", (car_w,car_h), asset_main_offset))
   asset_list.append(trees[tree_amount])
   tree_amount += 1

#LoadInstance
#lives
live1 = health_bar("Heart_1.png", (lives_size), (lives_location))
lieve2 = health_bar("Heart_2.png", (lives_size), (lives_location))
lieve3 = health_bar("Heart_3.png", (lives_size), (lives_location))
lieve4 = health_bar("Heart_4.png", (lives_size), (lives_location))
#loot
coin = loot("Coin.png", (50,50), -150, crash, 180, coin_score)
#player/Enemie
player1 = Player(Player_car, height -100, (car_w,car_h))
enemiecar1 = enemie(enemie_car_png, (car_w,car_h), -150, crash,180)
enemiecar1 = enemie(enemie_car_png, (car_w,car_h), -150, crash,180)
#Background
grass_background = Background((grass_green),0,0,width,height)
street_background =Background((street_gray),width/2-road_w/2,0,road_w,height )
right_boardermarking = Background((boarder_white), width/2 + road_w/2 - roadmark_w * 3, 0, roadmark_w, height )
left_boardermarking = Background((boarder_white), width/2 - road_w/2 + roadmark_w * 2, 0, roadmark_w, height)
middle = middle_line("Bomb.png", (90, 90), -50)
#Buttons
resume_button = button.Button(width/2-(191/2), height/4,resume_img,1)
quit_button = button.Button(width/2-(128/2), height/4+240, quit_img, 1)


#draw
player1.player_draw()
enemiecar1.enemie_draw()
coin.loot_draw()
middle.middle_line_draw()

#random draw the assets
for i in range(len(asset_list)):
    asset_list[i].asset_draw()


#Main Variables
counter = 0 
clock = pygame.time.Clock()
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer, 900 )
run = True

channel2 = pygame.mixer.Channel(1)
#channel1.play(theme_sound)
theme_sound.play()

#MainLoop
while run:

    clock.tick(FPS)
    
    grass_background.back_drawing()
    street_background.back_drawing()
    right_boardermarking.back_drawing()
    left_boardermarking.back_drawing()
    Info_lbl = Labels(str("Press Space  "),50, (255,255,255), (width - grass_right, height/4))
    Info_lbl1 = Labels(str(" for Pause "),50, (255,255,255), (width - grass_right, height/4+50))


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
                print("Space")
        if event.type == QUIT:
            run = False
            break 
   
    #check game state paused
    if game_paused == True:
        money = Labels(str(int(score)), 50, (255,255,255), (width/2, 110))
        money.label_draw()
        if resume_button.draw(window):
            if main_lives ==0:
                score=0
                main_lives = 4
                Level  = 0
                speed = 5 #change also main variable
                game_paused = False
            else:
                game_paused = False
        if quit_button.draw(window):
            run = False

    else:
        player1.player_movement()
        
        counter += 1
        if counter == 250:
            speed += 1
            Level += 1
            counter = 0 

        #if event.type == obstacle_timer:
            #enemiecar1.enemie_movement()

        #Collision Player/Enemiecar
        if player1.mask.overlap(enemiecar1.mask, (enemiecar1.loc.x  - player1.loc.x , enemiecar1.loc.y - player1.loc.y)):
            if crash == False:
                print("Crash")
                main_lives -= 1
                crash = True
               
        # Background drawing
        middle.middle_line_move()
        #assets movement
        for i in range(len(asset_list)):
            asset_list[i].asset_movement()
            asset_collision(asset_list)
        
        #asset_collision(asset_list)

        #Player movement
        enemiecar1.enemie_movement()

        #loot
        coin.loot_movement()
        coin.car_collision()
        
        #HealthBar
        if main_lives == 4:
            lieve4.lives_draw()
        elif main_lives == 3:
            lieve3.lives_draw()
        elif main_lives == 2:
            lieve2 .lives_draw()
        elif main_lives == 1:
            live1.lives_draw()
        elif main_lives == 0:
            print("Game Over")
            game_paused = True

        

        #labels
        speed_lbl = Labels(str("Level "+ str(Level)), 20, (255,255,255), (width/2, 70))
        #counter_lbl = Labels(str(counter), 20, (255,255,255), (width/2, 50))
        #fps_lbl = Labels(str(int(clock.get_fps())), 20, (255,255,255), (width/2, 80))
        money = Labels(str(int(score)), 50, (255,255,255), (width/2, 110))

    
        speed_lbl.label_draw()
        #counter_lbl.label_draw()
        #fps_lbl.label_draw()
        money.label_draw()    
        Info_lbl.label_draw()
        Info_lbl1.label_draw()

   
    pygame.display.update()
    
pygame.quit