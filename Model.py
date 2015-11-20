import pygame
from random import randint
from CustomVector import VectorCustom
from Features import FeatureExtractor
from QlearningAgent import AproximateQAgent
import math
import copy

from utils import *
__author__ = 'aferral'


NumAccion=30
margin = 20


class Obstacle():

    def __init__(self,radio,x,y):
        #Variables modelo
        self.velX = 2
        self.velY = 2
        self.velModulo=5
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        self.radio = radio
        self.player = False
        self.isComida = False

        self.northPoint = (0,0)



        self.distVision = self.radio * 600
        self.anguloAct = 0
        self.anguloVision = math.pi / 180.0 * 90
        self.anguloGiro =math.pi / 180.0 *360/NumAccion


        self.lastTime = 0

        #Variables visualizacion
        self.screen = None
        self.color = (0,0,0)

    def setPlayer(self):
        self.player = True
        self.color = (255,0,0)
        self.radio = 5
        self.distVision = self.radio + 10

    def teleport(self,point):
        self.x = point[0]
        self.y = point[1]

    def changeSpeed(self,velTuple):
        self.velX = velTuple[0]
        self.velY = velTuple[1]

    def Perseguir(self, objbueno):
        self.anguloAct = math.atan((objbueno.y-self.y)/(objbueno.x-self.x))
        self.velY = math.sin(self.anguloAct)*self.velModulo
        self.velX = math.cos(self.anguloAct)*self.velModulo

    def update(self,time):
        delta = time
        self.x += (self.velX*delta*200)
        self.y += (self.velY*delta*200)
        self.lastTime += delta
        pass
    def toStart(self):
        self.x = self.startX
        self.y = self.startY

    def setDraw(self,screen):
        self.screen = screen
        pass
    def draw(self):
        if self.screen != None:
            pygame.draw.circle(self.screen,self.color,(int(self.x),int(self.y)),self.radio,1)
        if self.player:
            pygame.draw.line(self.screen, (0,0,0), (int(self.x),int(self.y)), self.northPoint, 1)

    def setNorth(self,point):
        self.northPoint = point
    def newAngle(self,angle):
        self.anguloAct = angle
    def bounce(self):
        self.anguloAct -= 90

    #cree esta funcion para saber si esta en el angulo de vision
    def estaenvision(self,objm):
        angulo = math.atan2(objm.y-self.y,objm.x-self.x)*180/math.pi
        if angulo <0:
            angulo=angulo+360
        if self.anguloAct-self.anguloVision<angulo and angulo<self.anguloVision+self.anguloAct:
            return True
        return False

class JuegoModelo:
    def __init__(self):



        #Variables del modelo
        self.countDeath = 0
        self.iteraciones = 0
        self.score = 0

        self.listaObstaculos = []
        self.listaPersecutores =[]

        self.estadoActual = self.listaObstaculos
        self.estadoAnt = self.listaObstaculos

        self.lastAction = 0
        self.lastRew = 0

        self.planner = AproximateQAgent(self)

        #Cosas de bordes
        width = 800
        heigth = 600
        self.borders = [margin,width-margin,margin,heigth-margin]
        self.borders1 = [0,width,heigth,0]
        self.borders2 = [0,width,heigth,0   ]
        self.dim = (width,heigth)

        self.traspasarPared= True;

        self.p1 = (self.borders[0],self.borders[2])
        self.p2 = (self.borders[0],self.borders[3])
        self.p3 = (self.borders[1],self.borders[3])
        self.p4 = (self.borders[1],self.borders[2])

        #Features
        self.features = FeatureExtractor(self)

        self.featFun = None
        self.ended = False

        #Setear jugador
        playerObj = Obstacle(30,100,100)
        jugadorradio=playerObj.radio
        jugadorradio=0
        self.borders2 = [0+ jugadorradio,width- jugadorradio,heigth- jugadorradio,0+ jugadorradio]

        playerObj.setPlayer()

        self.listaObstaculos.append(playerObj)
        self.superestados=[0 for i in range(NumAccion)]

        #features y sus dimensiones
        self.dictFeatures = {'justDist'      :   (self.features.justDistFeature,2),
                        'borderDist'    :   (self.features.bordAndDistFeature,3),
                        'foodDist'      :   (self.features.comiditas,4)}


        pass

    def trainModel(self,constTime,iterations):
        print "Starting training of ",iterations
        print "Weights ",self.planner.weights
        self.planner.setEpsilon(0.8)
        for i in range(iterations):
            self.updateGame(constTime)
        self.planner.setEpsilon(0)
        print "Traing has ended ",self.planner.weights

        return self.planner.weights

    def testModel(self,constTime,iterations):
        print "Starting test of ",iterations
        print "Weights ",self.planner.weights
        for i in range(iterations):
            self.updateGame(constTime)
        print "Traing has ended el score es ",self.score
        pass

    def validateModel(self):
        pass


    def setWeight(self,weight):
        self.planner.weights = weight
        self.planner.setEpsilon(0)
        self.planner.endLearning()
    def VerifyPlayer(self,time,obj):
        for i in range(4):
            # bla = [self.borders[2],self.borders[3],self.borders[0],self.borders[1]]
            # pared=bla[i]
            pared=self.borders1[i]
            margin=pared
            if i == 0 and (pared-(obj.x)) > 0:
                #print "Choque en 0"
                obj.x = obj.x + self.borders1[1]
                #obj.velX *= -1
            if i == 1 and ((obj.x)- pared) > 0:
                #print "Choque en 1"
                obj.x = obj.x - margin
                #obj.velX *= -1
            if i == 2 and ((obj.y)- pared) > 0:
              #  print "Choque en 2"
                obj.y = obj.y - margin
               # obj.velY *= -1
            if i == 3 and (pared-(obj.y)) > 0:
              #  print "Choque en 3"
                obj.y = obj.y + self.borders1[2]
                #obj.velY *= -1
        # exit(1)

    def setFeatureArg(self,key):
        print "Colocando features ",key
        protoWeight = VectorCustom()
        (function,dimension) = self.dictFeatures[key]
        for elem in range(dimension):
            protoWeight.add(0)
        self.planner.weights = protoWeight
        self.setFeatureFun(function)


        pass


    def setFeatureFun(self,function):
        self.featFun = function

    def setFeatureFun(self,function):
        self.featFun = function

    def getFeatures(self,estado,accion):
        return self.featFun(estado,accion)


    def updateGame(self,tiempo):
        self.iteraciones += 1
        # print self.iteraciones

        self.estadoAnt = copy.deepcopy(self.listaObstaculos)

        playerObj = getPlayer(self.estadoActual)
        playerObj.update(tiempo)
        self.VerifyPlayer(tiempo, playerObj)

        #Hago todos lso mov
        for stalker in self.listaPersecutores:
            stalker.Perseguir(playerObj)

        for elem in self.listaObstaculos:
            if (elem.player == False) or (not(self.traspasarPared)):
                elem.update(tiempo)
                self.wallColl(elem)


        #Setear estado actual y ant
        self.estadoActual = self.listaObstaculos


        if self.ended:
            self.countDeath += 1
            #print "!!!!!!!!!!!!!!! Me mori !!!!!!!!!!!   ",self.countDeath

            self.ended = False
            playerObj = getPlayer(self.estadoActual)
            playerObj.toStart()
            return



        #Es el reward?
        reward = self.calculateReward(self.estadoActual)
        self.score += reward
        self.observe(self.estadoAnt,self.estadoActual,self.lastAction,reward)

        #Aca va el observe
        self.doAction(self.estadoActual,self.planner.getBestAction(self.estadoActual))
        pass
    def calculateReward(self,estado):
        acumulative=0
        playerObj = getPlayer(estado)
        listaColisiones = self.colision(playerObj)

        if len(listaColisiones)>0:
            for obj in listaColisiones:
                if obj.isComida:
                    #print "Comio una comidita"
                    self.listaObstaculos.remove(obj)
                    acumulative += 1000
                else:
                    #print "COLLISION DETECTADA"
                    self.endGame()
                    acumulative += -1000
            return acumulative
        return -1
    def endGame(self): #Me complico resetear el juego simplemente mantendre la transicion plana
        self.ended = True
        pass
    def doAction(self,estado,action):
        playerObj = getPlayer(estado)

        playerObj.changeSpeed((playerObj.velModulo*math.cos(action),playerObj.velModulo*math.sin(action)))
        playerObj.newAngle(action)
        # playerObj.teleport(actionToPoint(playerObj,action))


        self.lastAction = action
        pass

    def observe(self,estadoAnt,estado,accion,recomensa):
        #print"vvvv",accion
        self.planner.update(estadoAnt,accion,estado,recomensa)
        pass
    def wallColl(self,obj):
        for i in range(4):
            # bla = [self.borders[2],self.borders[3],self.borders[0],self.borders[1]]
            # pared=bla[i]
            pared=self.borders1[i]
            margin=pared
            if i == 0 and (pared-(obj.x - obj.radio)) > 0:
               # print "Choque en 0"
                obj.x = obj.radio + margin
                obj.velX *= -1
                obj.bounce()
            if i == 1 and ((obj.x + obj.radio)- pared) > 0:
               # print "Choque en 1"
                obj.x = -obj.radio + margin
                obj.velX *= -1
                obj.bounce()
            if i == 2 and ((obj.y + obj.radio)- pared) > 0:
              #  print "Choque en 2"
                obj.y = -obj.radio + margin
                obj.velY *= -1
                obj.bounce()
            if i == 3 and (pared-(obj.y - obj.radio)) > 0:
              #  print "Choque en 3"
                obj.y = obj.radio + margin
                obj.velY *= -1
                obj.bounce()

        # exit(1)

        pass

    def colision(self,obj1):
        lista = []
        for obj in self.listaObstaculos:
            if (d(obj1,obj) < (obj1.radio + obj.radio) and obj1 != obj):
              #  print "COLLIDE"
                lista.append(obj)
        return lista

    def addPlayer(self):
        pass
    def newObstacle(self,x,y):
        obstacle=Obstacle(30,x,y)
        self.listaObstaculos.append(obstacle)
        pass
    def newFood(self,x,y):
        food=Obstacle(7,x,y)
        food.color=(0,255,0)
        food.velX = 0
        food.velY = 0
        food.changeSpeed((0,0))
        food.isComida=True
        self.listaObstaculos.append(food)
    def newPersecutor(self,x,y):
        obstacle=Obstacle(30,x,y)
        self.listaObstaculos.append(obstacle)
        self.listaPersecutores.append(obstacle)


    def generateRandomObs(self,n):

        for i in range(n):
            xcord = randint(self.borders[0],self.borders[1])
            ycord = randint(self.borders[2],self.borders[3])
            self.newObstacle(xcord,ycord)

        pass
    def generateRandomPersecutor(self,n):

        for i in range(n):
            xcord = randint(self.borders[0],self.borders[1])
            ycord = randint(self.borders[2],self.borders[3])
            self.newPersecutor(xcord,ycord)
        pass


    #estooo!!
    def generateRandomFoods(self, m):
        for i in range(m):
            xcord = randint(self.borders[0],self.borders[1])
            ycord = randint(self.borders[2],self.borders[3])
            self.newFood(xcord,ycord)

        pass
    def legalActions(self,estado):
        jugador= getPlayer(estado)
        ponderaciones=self.CalcularPonderacion()

        acciones=[]
        for index,angulo in enumerate(ponderaciones):
            deltaAngulo=angulo*jugador.anguloGiro
            auxangulo = deltaAngulo+jugador.anguloAct

            (newX,newY)= actionToPoint(jugador,auxangulo, self)
            if self.traspasarPared == False:
                #if (newX<self.borders2[1] and newX>self.borders2[0]) and (newY>self.borders2[3] and newY<self.borders2[2]):
                self.superestados[index]=((newX,newY))
                acciones.append(auxangulo)
                if angulo == 0:
                    jugador.setNorth((newX,newY))

                #else:
                    #self.superestados[index]=(None)
            else:
                self.superestados[index]=((newX,newY))
                acciones.append(auxangulo)
            if angulo == 0:
                jugador.setNorth((newX,newY))
        # print "LA salidoa es ",acciones
        #print "La salidoa es ",acciones,self.superestados
        if len(acciones) == 0:
            raise Exception("TIRO 0 ACCIONES");

        return acciones
    def CalcularPonderacion(self):
        return range(-4,5)