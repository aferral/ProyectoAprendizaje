from Model import JuegoModelo
from QlearningAgent import AproximateQAgent

from CustomVector import VectorCustom
import math
__author__ = 'aferral'

import itertools

#Generar modo debug con grideo

#Iteraciones modo antes de probar


#Todo Separar el fin de juego del juego, si se acaba el juego tirar el main dneuvo (guardando weights(


#Todo formalizar la cosa de las features nose hacer una clase o algo, ademas de una buena forma de
#Inicializar vectores peso


__author__ = 'aferral'
import pygame, random
import math
from random import randint
# Define some colors
WHITE = (255, 255, 255)

fps = 20
constTime = fps/1000.0




from pygame.locals import *
class JuegoVisual:
    def __init__(self,juegomodelo):

        #Variable prueba
        self.modoStep = False

        self.done = False
        self.juegomodelo = juegomodelo

        pygame.init()
        self.screen = pygame.display.set_mode(
            [self.juegomodelo.dim[0], self.juegomodelo.dim[1]],HWSURFACE|DOUBLEBUF|RESIZABLE)

        for elem in self.juegomodelo.listaObstaculos:
            elem.setDraw(self.screen)
        self.clock = pygame.time.Clock()

    def drawBorde(self):
        pygame.draw.line(self.screen, (0,255,0), self.juegomodelo.p1, self.juegomodelo.p2)
        pygame.draw.line(self.screen, (0,255,0), self.juegomodelo.p2, self.juegomodelo.p3)
        pygame.draw.line(self.screen, (0,255,0), self.juegomodelo.p3, self.juegomodelo.p4)
        pygame.draw.line(self.screen, (0,255,0), self.juegomodelo.p4, self.juegomodelo.p1)
        pass


    def loop(self):

        while not self.done:

            if self.modoStep:
                raw_input()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print "Izq"
                        self.juegomodelo.listaObstaculos[1].changeSpeed((-1,0))

                    if event.key == pygame.K_RIGHT:
                        print "Derecha"
                        self.juegomodelo.listaObstaculos[1].changeSpeed((1,0))
                    if event.key == pygame.K_UP:
                        print "Arriba"
                        self.juegomodelo.listaObstaculos[1].changeSpeed((0,-1))
                    if event.key == pygame.K_DOWN:
                        print "Down"
                        self.juegomodelo.listaObstaculos[1].changeSpeed((0,1))

                        pygame.display.flip()
            # Clear the screen
            self.screen.fill(WHITE)
            listaObjetos = self.juegomodelo.listaObstaculos
            self.juegomodelo.updateGame(constTime)
            for elem in listaObjetos:
                elem.draw()

            #Elementos auxiliares
            for point in self.juegomodelo.superestados:
                #print"pppp1",point
                if point == None:
                    continue
                #print "Punto sigiente ",point
                #print"pppp",point
                pygame.draw.circle(self.screen,(255,0,0),(int(point[0]),int(point[1])),2,1)

            self.drawBorde()
            # Limit to X frames per second
            self.clock.tick(fps)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        pygame.quit()
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(dest="nEnemies", type=int,help="Cuantos meteoros colocar", default=2, nargs='?')
parser.add_argument(dest='feature',help="0 feature dist, 1 featuresDistBorder", default=1, nargs='?')

args = parser.parse_args()


modelo = JuegoModelo()
modelo.generateRandomObs(args.nEnemies)
if args.feature:
    modelo.setBorderAndDistFeature()
vista = JuegoVisual(modelo)
vista.loop()
