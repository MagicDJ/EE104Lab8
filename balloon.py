# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:43:33 2022

@author: devin
"""
import pgzrun
import pygame
import pgzero
import random
from pgzero.builtins import Actor
from random import randint

WIDTH = 800
HEIGHT = 600

balloon = Actor("balloon")
balloon.pos = 400, 300

bird = Actor("bird-up")
bird.pos = randint(800, 1600), randint(10, 200)

house = Actor("house")
house.pos = randint(800, 1600), 460

tree = Actor("tree")
tree.pos = randint(800, 1600), 450

bird_up = True
up = False
game_over = False
score = 0
number_of_updates = 0

scores = []
lives = 3##tweak2 added lives to the game
hit=0## tweak2 serves as an indicator for collision
lvl=1## tweak4 Level up, Level indicator

def update_high_scores():
    global score, scores
    filename = r"high-scores.txt"##tweak1 added more high scores
    scores = []
    with open(filename, "r") as file:
        line = file.readline()
        high_scores = line.split()
        for high_score in high_scores:
            if(score > int(high_score)):
                scores.append(str(score) + " ")
                score = int(high_score)
            else:
                scores.append(str(high_score) + " ")
    with open(filename, "w") as file:
        for high_score in scores:
            file.write(high_score)

def display_high_scores():
    screen.draw.text("High Scores", (350, 150), color="black")
    y = 175
    position = 1
    for high_score in scores:
        screen.draw.text(str(position) + ". " + high_score, (350, y), color="black")
        y += 25
        position += 1

def lvlup():##tweak 4 define level up check when ever score is increased
    global lvl,score
    if score%10==0:##tweak 4 for every 10pts score, level increase by 1
        lvl +=1
        if lvl >10:##tweak 4 max level is set to 10
            lvl=10
            
def draw():
    screen.blit("background", (0,0))
    if not game_over:
        balloon.draw()
        bird.draw()
        house.draw()
        tree.draw()
        screen.draw.text("Score: " + str(score), (700, 5), color="black")
        screen.draw.text("Lives: " + str(lives), (700,20), color="red")##tweak 2
        screen.draw.text("Level: " + str(lvl), (0, 5), color="black")##tweak 4 
    else:
        display_high_scores()

def on_mouse_down():
    global up
    up = True
    balloon.y -= 50

def on_mouse_up():
    global up
    up = False

def flap():
    global bird_up
    if bird_up:
        bird.image = "bird-down"
        bird_up = False
    else:
        bird.image = "bird-up"
        bird_up = True
def update():
    global game_over, score, number_of_updates, lives, hit, lvl
    if not game_over:
        if not up:
            balloon.y += 1

        if bird.x > 0:
            bird.x -=(lvl*2)+8##tweak3 speed it up/tweak 4 increase difficulty each level
            if number_of_updates == 9:
                flap()
                number_of_updates == 0
            else:
                number_of_updates += 1

        else:
            bird.x = randint(800, 1600)
            bird.y = randint(10, 200)
            score += 1
            number_of_updates = 0
            lvlup()
        
        if house.right > 0:
            house.x -=(lvl*2)+4##tweak3 speed up house/tweak 4 increase difficulty each level
        else:
            house.x = randint(800, 1600)
            score += 1
            lvlup()
            
        if tree.right > 0:
            tree.x -=(lvl*2)+4##tweak3 speed up tree/tweak 4 increase difficulty each level
        else:
            tree.x = randint(800, 1600)
            score += 1
            lvlup()

        if balloon.top < 0 or balloon.bottom > 560:
            game_over = True
            update_high_scores()
        
        if balloon.collidepoint(bird.x, bird.y) or balloon.collidepoint(house.x, house.y) or \
            balloon.collidepoint(tree.x, tree.y):
                hit=hit-1##tweak2 when hit, the counter will tick
                if hit==-1:##when tick reaches a certain point, life is loss
                    lives=lives-1
                elif lives==0:##when lives reach 0, game over
                    game_over = True
                    update_high_scores()
        else:#when there is no collision reset hit counter
            hit=0


        
pgzrun.go()