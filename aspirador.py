#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 17:42:05 2019

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.

@author: Thiago da Silva Teixeira
"""

import sys
import os
import time
import pygame
import random

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
yellow   = ( 255, 255,   0)



class Bot():
    def __init__(self,x,y, filename, filename2):
       self.x = x
       self.y = y
       self.sprite = [get_image(filename), get_image(filename2)]

    def move(self):
        # limite 650 450
        while True:
            direction = random.randint(0,3)
            if direction == 0:
                if self.x > 50:
                    self.x += -100
                    break
            elif direction == 1:
                if self.x < 650:
                    self.x += 100
                    break
            elif direction == 2:
                if self.y > 50:
                    self.y += -100
                    break
            elif direction == 3:
                if self.y < 450:
                    self.y += 100
                    break

_sound_library = {}
def play_sound(path):
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
  sound.play()


_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image



def showFloor(floor):
    for l in floor:
        for c in l:
            # [0, [x,y]]
            print(str(c[0])+' ', end='')
        print('')

def fase(floor, maxApple, maxDog):
    # B base
    # A apple
    # D dog

    floor[0][0][0] = 'B'
    linha = len(floor)-1
    coluna = len(floor[0])-1

    nApple = random.randint(1, maxApple)
    nDog = random.randint(1, maxDog)

    i = 0
    while i != nApple:
        x = random.randint(1,linha)
        y = random.randint(1,coluna)
        if floor[x][y][0] == '0':
            floor[x][y][0] = 'A'
            i += 1

    i = 0
    while i != nDog:
        x = random.randint(1,linha)
        y = random.randint(1,coluna)
        if floor[x][y][0] == '0':
            floor[x][y][0] = 'D'
            i += 1

    return floor

def dVector(x,y,i,j):
    if x-i != 0:
        if x-i > 0:
            return [-1,0]
        else:
            return [1,0]
    elif y-j != 0:
        if y-j > 0:
            return [0,-1]
        else:
            return [0,1]

def buscaLargura(floor, nApple, busca):
    random.shuffle(busca)

    while True:
        buscaFiltrada = []
        while(len(busca) != 0):
            caso = busca.pop()
            if caso is None: continue
            x,y = caso[-1]

            # é valido?
            if floor[x][y][0] == 'D': continue

            if floor[x][y][0] == 'B' and len(caso) > 1:
                count = 0
                for c in caso:
                    if floor[c[0]][c[1]][0] == 'A':
                        count += 1
                if count == nApple:
                    return True, caso
                else:
                    # rejeita
                    continue

            if x+1 <= (len(floor)-1):
                if (x+1, y) not in caso or (x, y-1) == (0,0):
                    buscaFiltrada.append(caso+[(x+1, y)])
            if x-1 >= 0:
                if (x-1, y) not in caso or (x, y-1) == (0,0):
                    buscaFiltrada.append(caso+[(x-1, y)])
            if y+1 <= (len(floor[0])-1):
                if (x, y+1) not in caso or (x, y-1) == (0,0):
                    buscaFiltrada.append(caso+[(x, y+1)])
            if y-1 >= 0:
                if (x, y-1) not in caso or (x, y-1) == (0,0):
                    buscaFiltrada.append(caso+[(x, y-1)])

        busca = buscaFiltrada
        if len(buscaFiltrada) == 0: return False, []

def acharDirecao(solucao, arrows):
    map = {'-10':arrows[2],
            '10':arrows[3],
            '01':arrows[1],
            '0-1':arrows[0]
    }

    direcao = []
    for i in range(1,len(solucao)):
        x,y = solucao[i-1][0] - solucao[i][0], solucao[i-1][1] - solucao[i][1]
        direcao.append(map[str(x)+str(y)])

    return direcao


pygame.init()
pygame.display.set_caption('O comedor de maçã')
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))



BLOCK_SIZE = 100

clock = pygame.time.Clock()
pygame.display.update()

SPEED = 5

player = Bot(100,100,'imagens/robot.png', 'imagens/robot_love.png')

applesRespawn = 0
appleSprite = get_image('imagens/apple.png')
dogSprite = get_image('imagens/dog.png')
baseSprite = get_image('imagens/base.png')

robotWin = get_image('imagens/robot_win.png')
robotLose = get_image('imagens/robot_lose.png')
robotAwake = get_image('imagens/robot_awake.png')

impossibleSprite = get_image('imagens/impossible.png')

esquerdaSprite = get_image('imagens/esquerda.png')
direitaSprite = get_image('imagens/direita.png')
cimaSprite = get_image('imagens/cima.png')
baixoSprite = get_image('imagens/baixo.png')
arrows = [esquerdaSprite,direitaSprite,cimaSprite,baixoSprite]

robotThinking = get_image('imagens/robot-thinking.png')
background = get_image('imagens/back.jpg')
apples = []

loveBool = False


message = pygame.mixer.Sound('sound/message.wav')
wrong = pygame.mixer.Sound('sound/wrong.wav')
correct = pygame.mixer.Sound('sound/correct.wav')
coin = pygame.mixer.Sound('sound/coin.wav')

vector = [0,0]

#ok
while True:
    intro = True
    while intro:
        floor = [[ ['0',[x,y]] for x in range(100,800,100)] for y in range(100,600,100)]
        floor = fase(floor, 5, 5)
        showFloor(floor)
        nApple = ([y[0] for x in floor for y in x]).count("A")

        #screen.fill(white)
        screen.blit(background, (0, 0))

        screen.blit(player.sprite[0], (50, 50))

        for i in floor:
            for j in i:
                if j[0] == "0":continue
                if j[0] == 'A': screen.blit(appleSprite, (j[1][0]-50, j[1][1]-50))
                if j[0] == 'D': screen.blit(dogSprite, (j[1][0]-50, j[1][1]-50))


        screen.blit(robotThinking, (700, 500))
        pygame.display.flip()

        ok,solucao = buscaLargura(floor, nApple, [ [(0,0) ]])
        if ok:
            intro = False
            print(solucao)
        else:
            print("Não existe solução")
            #screen.fill(white)
            screen.blit(background, (0, 0))
            for i in floor:
                for j in i:
                    if j[0] == "0":continue
                    if j[0] == 'A': screen.blit(appleSprite, (j[1][0]-50, j[1][1]-50))
                    if j[0] == 'D': screen.blit(dogSprite, (j[1][0]-50, j[1][1]-50))
            screen.blit(robotLose, (50, 50))
            screen.blit(impossibleSprite, (200, 30))
            wrong.play()
            pygame.display.flip()
            time.sleep(3)


    correct.play()
    #
    caminho = solucao.copy()
    destinyX, destinyY = caminho.pop()
    destinyX, destinyY = caminho.pop()
    destinyX, destinyY = floor[destinyX][destinyY][1]
    vector = dVector(player.x, player.y, destinyX, destinyY)
    vector = [vector[0]*SPEED,vector[1]*SPEED]

    direcao = acharDirecao(solucao, arrows)

    #

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        ####
        #screen.fill(white)
        screen.blit(background, (0, 0))

        #Base
        #pygame.draw.circle(screen, black, (100, 100) , 10)
        screen.blit(baseSprite, (50,50))

        i = 0
        for passo in solucao[1:]:
            if passo != (0,0):
                x,y = floor[passo[0]][passo[1]][1]
                screen.blit(direcao[i], (x-25,y-25))
                i += 1


        for l in floor:
            for c in l:
                if c[0] in ['0','B']: continue
                if c[0] == 'A': screen.blit(appleSprite, (c[1][0]-50,c[1][1]-50))
                elif c[0] == 'D': screen.blit(dogSprite, (c[1][0]-50,c[1][1]-50))


        if False:
            for x in range(100,800,100):
                for y in range(100,600,100):
                    pygame.draw.circle(screen, black, (x+100,y+100) , 10)

        if loveBool:
            screen.blit(player.sprite[1], (player.x-50, player.y-50))
            pygame.display.flip()
            time.sleep(0.5)
            loveBool = False
            continue


        if [player.x, player.y] != [destinyX, destinyY]:
            player.x += vector[0]
            player.y += vector[1]

        else:
            # final
            if len(caminho) == 0:
                message.play()
                done = True
                screen.blit(robotWin, (player.x-50, player.y-50))
                pygame.display.flip()
                time.sleep(2)
                break
            #novo destino
            destinyX, destinyY = caminho.pop()
            destinyX, destinyY = floor[destinyX][destinyY][1]
            vector = dVector(player.x, player.y, destinyX, destinyY)
            vector = [vector[0]*SPEED,vector[1]*SPEED]
            if floor[int(player.y/100)-1][int(player.x/100)-1][0] == 'A':
                floor[int(player.y/100)-1][int(player.x/100)-1][0] = '0'
                loveBool = True
                coin.play()


        screen.blit(robotAwake, (player.x-50, player.y-50))

        pygame.display.flip()

        clock.tick(60)


time.sleep(1)

pygame.quit()
