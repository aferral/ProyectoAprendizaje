__author__ = 'aferral'

"""
armar clase obstaculo
clase jugador contiene cordenadas

movimiento input

algoritmos de movimiento de obstaculos
obstaculos que sigan al jugador
formas de diferenciar obstaculos




ciclo que dibuja todo
"""

import itertools

__author__ = 'aferral'
import pygame, random
import math
from random import randint
# Define some colors
WHITE = (255, 255, 255)
margin = 20


class Obstacle():

    def __init__(self,radio,x,y):
        #Variables modelo
        self.velX = 1
        self.velY = 1
        self.x = x
        self.y = y
        self.radio = radio
        self.player = False

        self.lastTime = 0

        #Variables visualizacion
        self.screen = None
        self.color = (0,0,255)

    def setPlayer(self):
        self.player = True
        self.color = (255,0,0)
    def changeSpeed(self,velTuple):
        self.velX = velTuple[0]
        self.velY = velTuple[1]

    def update(self,time):
        delta = (time - self.lastTime) * 0.1
        self.x += int(self.velX*delta)
        self.y += int(self.velY*delta)
        self.lastTime = time
        pass

    def setDraw(self,screen):
        self.screen = screen
        pass
    def draw(self):
        if self.screen != None:
            pygame.draw.circle(self.screen,self.color,(self.x,self.y),self.radio,1)

class JuegoModelo:
    def __init__(self):
        self.listaObstaculos = []


        width = 800
        heigth = 600
        self.borders = [margin,width-margin,margin,heigth-margin]
        self.borders1 = [0,width,heigth,0]
        self.dim = (width,heigth)


        #Setear jugador
        self.playerObj = Obstacle(5,100,100)
        self.playerObj.setPlayer()

        self.listaObstaculos.append(self.playerObj)



        pass
    def wallColl(self,obj):
        print "POsicion objeto",obj.x,obj.y
        for i in range(4):
            # bla = [self.borders[2],self.borders[3],self.borders[0],self.borders[1]]
            # pared=bla[i]
            pared=self.borders1[i]
            margin=pared
            print i,pared
            if i == 0 and (pared-(obj.x - obj.radio)) > 0:
                print "Choque en 0"
                obj.x = obj.radio + margin
                obj.velX *= -1
            if i == 1 and ((obj.x + obj.radio)- pared) > 0:
                print "Choque en 1"
                obj.x = -obj.radio + margin
                obj.velX *= -1
            if i == 2 and ((obj.y + obj.radio)- pared) > 0:
                print "Choque en 2"
                obj.y = -obj.radio + margin
                obj.velY *= -1
            if i == 3 and (pared-(obj.y - obj.radio)) > 0:
                print "Choque en 3"
                obj.y = obj.radio + margin
                obj.velY *= -1
        # exit(1)

        pass

    def colision(self,obj1):
        for obj in self.listaObstaculos:
            if self.d(obj1,obj) > (obj1.radio + obj.radio):
                return True
        return False
    def d(self,obj1,obj2):
        return math.sqrt(math.pow((obj1.x-obj2.x),2)+math.pow((obj1.y-obj2.y),2))
    def addPlayer(self):
        pass
    def newObstacle(self,x,y):
        self.listaObstaculos.append(Obstacle(5,x,y))
        pass
    def generateRandomObs(self,n):

        for i in range(n):
            xcord = randint(self.borders[0],self.borders[1])
            ycord = randint(self.borders[2],self.borders[3])
            self.newObstacle(xcord,ycord)

        pass
class JuegoVisual:
    def __init__(self,juegomodelo):
        self.done = False
        self.juegomodelo = juegomodelo

        pygame.init()
        self.screen = pygame.display.set_mode(
            [self.juegomodelo.dim[0], self.juegomodelo.dim[1]])

        for elem in self.juegomodelo.listaObstaculos:
            elem.setDraw(self.screen)
        self.clock = pygame.time.Clock()


    def drawBorde(self):
        bordes = self.juegomodelo.borders
        p1 = (bordes[0],bordes[2])
        p2 = (bordes[0],bordes[3])
        p3 = (bordes[1],bordes[3])
        p4 = (bordes[1],bordes[2])
        pygame.draw.line(self.screen, (0,255,0), p1, p2)
        pygame.draw.line(self.screen, (0,255,0), p2, p3)
        pygame.draw.line(self.screen, (0,255,0), p3, p4)
        pygame.draw.line(self.screen, (0,255,0), p4, p1)
        pass


    def loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print "Izq"
                        self.juegomodelo.playerObj.changeSpeed(1,0)
                    if event.key == pygame.K_RIGHT:
                        print "Derecha"
                        self.juegomodelo.playerObj.changeSpeed(-1,0)
                    if event.key == pygame.K_UP:
                        print "Arriba"
                        self.juegomodelo.playerObj.changeSpeed(0,1)
                    if event.key == pygame.K_DOWN:
                        print "Down"
                        self.juegomodelo.playerObj.changeSpeed(0,-1)
            # Clear the screen
            self.screen.fill(WHITE)
            listaObjetos = self.juegomodelo.listaObstaculos
            for elem in listaObjetos:
                elem.update(pygame.time.get_ticks())
                self.juegomodelo.wallColl(elem)
                elem.draw()

            self.drawBorde()
            # Limit to 60 frames per second
            self.clock.tick(15)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        pygame.quit()

modelo = JuegoModelo()
modelo.generateRandomObs(0)
vista = JuegoVisual(modelo)
vista.loop()