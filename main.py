from QlearningAgent import AproximateQAgent
import copy
from CustomVector import VectorCustom
import math
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
#
import itertools

__author__ = 'aferral'
import pygame, random
import math
from random import randint
# Define some colors
WHITE = (255, 255, 255)
margin = 20

def d(obj1,obj2):
    return math.sqrt(math.pow((obj1.x-obj2.x),2)+math.pow((obj1.y-obj2.y),2))
def getAngle(obj1,obj2):
    return math.atan2(obj2.y,obj2.x)-math.atan2(obj1.y,obj1.x)

def getAngleFromOrigin(origin,orgRot,obj):
    return

class Obstacle():

    def __init__(self,radio,x,y):
        #Variables modelo
        self.velX = 1
        self.velY = 1
        self.x = x
        self.y = y
        self.radio = radio
        self.player = False

        self.distVision = self.radio * 10
        self.anguloAct = 0
        self.anguloVision = math.pi / 180.0 * 90
	self.anguloGiro =math.pi / 180.0 *10


        self.lastTime = 0

        #Variables visualizacion
        self.screen = None
        self.color = (0,0,255)

    def setPlayer(self):
        self.player = True
        self.color = (255,0,0)
        self.velX *= 2
        self.velY *= 2
    def changeSpeed(self,velTuple):
        self.velX = velTuple[0]
        self.velY = velTuple[1]

    def update(self,time):
    	#cambair a dt;
        delta = self.deltaTime
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
    #cree esta funcion para saber si esta en el angulo de vision 
    def estaenvision(self,objm)
	    angulo=atan2(objm.y-self.y,objm.x-self.x)*180/math.pi
	    if angulo <0
		    angulo=angulo+360
	    if self.anguloAct-self.anguloVision<angulo and angulo<self.anguloVision+self.anguloAct
	    	return True
	    return False

class JuegoModelo:
    def __init__(self):
        self.listaObstaculos = []

        self.estadoActual = self.listaObstaculos
        self.estadoAnt = self.listaObstaculos

        self.lastAction = None
        self.lastRew = 0

        self.planner = AproximateQAgent(self)

        width = 800
        heigth = 600
        self.borders = [margin,width-margin,margin,heigth-margin]
        self.borders1 = [0,width,heigth,0]
        self.dim = (width,heigth)
	self.deltaTime=15/1000.0

	#agrego acciones para elejir mejor q value
	self.superestados=[0,0,0,0,0]

        #Setear jugador
        self.playerObj = Obstacle(5,100,100)
        self.playerObj.setPlayer()

        self.listaObstaculos.append(self.playerObj)



        pass
    def getFeatures(self):
        dVis = self.playerObj.distVision
        mindist = dVis
        for obj in self.listaObstaculos:
            if obj != self.playerObj and (d(obj,self.playerObj) < dVis):
            	#Agregue la funcion para saber el angulo 
                if (self.playerObj.estaenvision(obj)):
                    mindist = min(mindist,d(obj,self.playerObj))
        vec = VectorCustom().add(mindist)
        return vec

    def updateGame(self,tiempo):

        self.estadoAnt = copy.deepcopy(self.listaObstaculos)

        #Hago todos lso mov
        for elem in self.listaObstaculos:
            elem.update(tiempo)
            self.wallColl(elem)

        #Setear estado actual y ant
        self.estadoActual = self.listaObstaculos
	
	#Es el reward?
        reward = self.calculateRew()
        self.observe(self.estadoAnt,self.estadoActual,self.lastAction,reward)

        #Aca va el observe
        self.doAction(self.planner.getBestAction(self.estadoActual))


        pass
    def calculateReward(self):

        if self.colision(self.playerObj):
            self.endGame()
            return -9999999999
        return 0

    def doAction(self,action):
        self.playerObj.x = action[0]
        self.playerObj.y = action[1]
        self.playerObj.anguloAct = action[2]
        pass

    def observe(self,estadoAnt,estado,accion,recomensa):
        self.planner.update(estadoAnt,accion,estado,recomensa)
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
            if d(obj1,obj) > (obj1.radio + obj.radio):
                return True
        return False

    def addPlayer(self):
        pass
    def newObstacle(self,x,y):
        self.listaObstaculos.append(Obstacle(10,x,y))
        pass
    def generateRandomObs(self,n):

        for i in range(n):
            xcord = randint(self.borders[0],self.borders[1])
            ycord = randint(self.borders[2],self.borders[3])
            self.newObstacle(xcord,ycord)

        pass
    #estooo!!
    def legalActions(self):
    	jugador=self.playerObj
    	self.borders1
    	ponderaciones=[-2,-1,0,1,2]
    	acciones=[]
    	for i in ponderaciones:
    		auxangulo=i*jugador.anguloGiro+jugador.anguloAct
    		velModulo=math.sqrt(jugador.velX**2+jugador.velY**2)
    		deltaX= self.deltaTime*velModulo*cos(auxangulo)
		deltaY= self.deltaTime*velModulo*sin(auxangulo)
		newX=jugador.x + deltaX
    		newY=jugador.y + deltaY
    		if (newX<self.borders1[2] and newX>self.borders1[3]) and (newY>self.borders1[0] and newY<self.borders1[1]):
    			self.superestados[i+2]=(deltaX,deltaY)
    			acciones.append(auxangulo)
    		else:
    			self.superestados[i+2]=(None)
    	return acciones
    	
    	
class JuegoVisual:
    def __init__(self,juegomodelo):
        self.done = False
        self.juegomodelo = juegomodelo

        pygame.init()
        self.screen = pygame.display.set_mode(
            [self.juegomodelo.dim[0], self.juegomodelo.dim[1]])
	#agrego variable que sabe cuales son las acciones
	
	self.

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

            self.juegomodelo.updateGame(pygame.time.get_ticks())
            for elem in listaObjetos:
                elem.draw()

            self.drawBorde()
            # Limit to 60 frames per second
            self.deltaTime = self.clock.tick(15)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        pygame.quit()

modelo = JuegoModelo()
modelo.generateRandomObs(10)
vista = JuegoVisual(modelo)
vista.loop()
