import pygame
from random import randint
from CustomVector import VectorCustom
from QlearningAgent import AproximateQAgent
import math
import copy

__author__ = 'aferral'


NumAccion=10
margin = 20

def d(obj1,obj2):
    return math.sqrt(math.pow((obj1.x-obj2.x),2)+math.pow((obj1.y-obj2.y),2))
def distance(x1,y1,x2,y2):
    return math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))

def getAngle(obj1,obj2):
    return math.atan2(obj2.y,obj2.x)-math.atan2(obj1.y,obj1.x)

def actionToPoint(obj,action):
    deltaX= obj.velModulo*math.cos(action)*4
    deltaY= obj.velModulo*math.sin(action)*4
    FuturoX=obj.x + deltaX
    FuturoY=obj.y + deltaY
    return (FuturoX,FuturoY)

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

        self.distVision = self.radio * 600
        self.anguloAct = 0
        self.anguloVision = math.pi / 180.0 * 90
        self.anguloGiro =math.pi / 180.0 *360/NumAccion


        self.lastTime = 0

        #Variables visualizacion
        self.screen = None
        self.color = (0,0,255)

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
        # if self.player:
        #     pygame.draw.circle(self.screen,(0,255,0),(int(self.x),int(self.y)),self.distVision,1)


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

        self.listaObstaculos = []

        self.estadoActual = self.listaObstaculos
        self.estadoAnt = self.listaObstaculos

        self.lastAction = 0
        self.lastRew = 0

        self.planner = AproximateQAgent(self)

        #Cosas de bordes
        width = 400
        heigth = 500
        self.borders = [margin,width-margin,margin,heigth-margin]
        self.borders1 = [0,width,heigth,0]
        self.borders2 = [0,width,heigth,0]
        self.dim = (width,heigth)

        self.p1 = (self.borders[0],self.borders[2])
        self.p2 = (self.borders[0],self.borders[3])
        self.p3 = (self.borders[1],self.borders[3])
        self.p4 = (self.borders[1],self.borders[2])


        self.featFun = None
        self.setJustDistFeature()
        self.ended = False

        #Setear jugador
        playerObj = Obstacle(30,100,100)
        jugadorradio=playerObj.radio
        jugadorradio=0
        self.borders2 = [0+ jugadorradio,width- jugadorradio,heigth- jugadorradio,0+ jugadorradio]

        playerObj.setPlayer()

        self.listaObstaculos.append(playerObj)
        self.superestados=[0 for i in range(NumAccion)]



        pass

    def setFeatureFun(self,function):
        self.featFun = function

    def setJustDistFeature(self):

        protoWeight = VectorCustom()
        protoWeight.add(0)
        protoWeight.add(0)

        self.planner.weights = protoWeight
        self.setFeatureFun(self.justDistFeature)

    def setBorderAndDistFeature(self):
        protoWeight = VectorCustom()
        protoWeight.add(0)
        protoWeight.add(0)
        protoWeight.add(0)

        self.planner.weights = protoWeight
        self.setFeatureFun(self.bordAndDistFeature)

    def getPlayer(self,estado):
        return estado[0]


    def justDistFeature(self,estado,accion):
        playerObj = self.getPlayer(estado)
        mindist = 9999
        vec = VectorCustom()
        distNextStep = mindist
        (FuturoX,FuturoY) = actionToPoint(playerObj,accion)

        for obj in estado:
            if obj != playerObj :
                Xaux=obj.x
                Yaux=obj.y
                mindist=min(mindist,distance(FuturoX,FuturoY,Xaux,Yaux))

        vec.add(10/(mindist))
        vec.add(1)
        return vec
    def bordAndDistFeature(self,estado,accion):

        playerObj = self.getPlayer(estado)
        mindist = 9999
        vec = VectorCustom()
        distNextStep = mindist
        (FuturoX,FuturoY) = actionToPoint(playerObj,accion)

        for obj in estado:
            if obj != playerObj :
                Xaux=obj.x
                Yaux=obj.y
                mindist=min(mindist,distance(FuturoX,FuturoY,Xaux,Yaux))


        #Tambien calcula la distancia al board mas cercano
        #Calcula distncias a lines que representar bordes
        #p1-----------------------------p2
        #-                              -
        #-                              -
        #-                              -
        #-                              -
        #-                              -
        #p4-----------------------------p3


        distC1 = distance(FuturoX,FuturoY,self.p1[0],self.p1[1])
        distC2 = distance(FuturoX,FuturoY,self.p2[0],self.p2[1])
        distC3 = distance(FuturoX,FuturoY,self.p3[0],self.p3[1])
        distC4 = distance(FuturoX,FuturoY,self.p4[0],self.p4[1])

        print "Cordinates ",(FuturoX,FuturoY)
        print "p1 - p3 ",self.p1," ",self.p3
        print "Distancia bordes "
        print "DistC1 ",distC1
        print "DistC2 ",distC2
        print "DistC3 ",distC3
        print "DistC4 ",distC4

        minBor = min(distC1,distC2,distC3,distC4)
        # print "Distancia a Borde mas cercano ",minBor

        vec.add(3/(minBor+0.1))
        vec.add(10/(mindist))
        vec.add(1)
        return vec

    def getFeatures(self,estado,accion):
        return self.featFun(estado,accion)


    def updateGame(self,tiempo):
        self.iteraciones += 1

        self.estadoAnt = copy.deepcopy(self.listaObstaculos)


        #Hago todos lso mov
        for elem in self.listaObstaculos:

            elem.update(tiempo)
            self.wallColl(elem)

        #Setear estado actual y ant
        self.estadoActual = self.listaObstaculos

        if self.ended:
            self.countDeath += 1
            print "!!!!!!!!!!!!!!! Me mori !!!!!!!!!!!   ",self.countDeath

            self.ended = False
            playerObj = self.getPlayer(self.estadoActual)
            playerObj.toStart()
            return



        #Es el reward?
        reward = self.calculateReward(self.estadoActual)
        self.observe(self.estadoAnt,self.estadoActual,self.lastAction,reward)

        #Aca va el observe
        self.doAction(self.estadoActual,self.planner.getBestAction(self.estadoActual))
        pass

    def calculateReward(self,estado):
        playerObj = self.getPlayer(estado)
        if self.colision(playerObj):
            print "COLLISION DETECTADA"
            self.endGame()
            return -1000
        return 1
    def endGame(self): #Me complico resetear el juego simplemente mantendre la transicion plana
        self.ended = True
        pass
    def doAction(self,estado,action):
        playerObj = self.getPlayer(estado)

        playerObj.changeSpeed((playerObj.velModulo*math.cos(action),playerObj.velModulo*math.sin(action)))
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
            if i == 1 and ((obj.x + obj.radio)- pared) > 0:
               # print "Choque en 1"
                obj.x = -obj.radio + margin
                obj.velX *= -1
            if i == 2 and ((obj.y + obj.radio)- pared) > 0:
              #  print "Choque en 2"
                obj.y = -obj.radio + margin
                obj.velY *= -1
            if i == 3 and (pared-(obj.y - obj.radio)) > 0:
              #  print "Choque en 3"
                obj.y = obj.radio + margin
                obj.velY *= -1
        # exit(1)

        pass

    def colision(self,obj1):
        for obj in self.listaObstaculos:
            if (d(obj1,obj) < (obj1.radio + obj.radio) and obj1 != obj):
              #  print "COLLIDE"
                return True
        return False

    def addPlayer(self):
        pass
    def newObstacle(self,x,y):
        self.listaObstaculos.append(Obstacle(30,x,y))
        pass
    def generateRandomObs(self,n):

        for i in range(n):
            xcord = randint(self.borders[0],self.borders[1])
            ycord = randint(self.borders[2],self.borders[3])
            self.newObstacle(xcord,ycord)

        pass
    #estooo!!
    def legalActions(self,estado):
        jugador= self.getPlayer(estado)
        ponderaciones=self.CalcularPonderacion()
        acciones=[]
        for index,angulo in enumerate(ponderaciones):
            deltaAngulo=angulo*jugador.anguloGiro
            auxangulo = deltaAngulo+jugador.anguloAct

            (newX,newY)= actionToPoint(jugador,auxangulo)

            if (newX<self.borders2[1] and newX>self.borders2[0]) and (newY>self.borders2[3] and newY<self.borders2[2]):
                self.superestados[index]=((newX,newY))
                acciones.append(auxangulo)
            else:
                self.superestados[index]=(None)
        # print "LA salidoa es ",acciones
        if len(acciones) == 0:
            raise Exception("TIRO 0 ACCIONES");


        #print("tttttttttt"),acciones
        return acciones
    def CalcularPonderacion(self):
        return range(NumAccion)