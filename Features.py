from CustomVector import VectorCustom
from utils import *

__author__ = 'aferral'

class Feature:

    def __init__(self,modelo):
        self.p1 = modelo.p1
        self.p2 = modelo.p2
        self.p3 = modelo.p3
        self.p4 = modelo.p4
        self.modelo=modelo
        self.descriptor = []
        self.vector = VectorCustom()

    def getValue(self,estado,accion):
        raise NotImplemented

class justDistFeature(Feature):

    def __init__(self,modelo):
        Feature.__init__(self,modelo)
        self.descriptor = ["distObs","bias"]


    def getValue(self,estado,accion):
        playerObj = getPlayer(estado)
        mindist = 9999
        (FuturoX,FuturoY) = actionToPoint(playerObj,accion,self.modelo)

        for obj in estado:
            if obj != playerObj and obj.isComida == False:
                Xaux=obj.x
                Yaux=obj.y
                mindist=min(mindist,distance(FuturoX,FuturoY,Xaux,Yaux))

        self.vector.add("distObs",10/(mindist+0.1))
        self.vector.add("bias",1)
        return self.vector

class bordAndDistFeature(Feature):

    def __init__(self,modelo):
        Feature.__init__(self,modelo)
        self.descriptor = ["minDistBord","distObs","bias"]
    def getValue(self,estado,accion):

        self.vector = justDistFeature(self.modelo).getValue(estado,accion)
        playerObj = getPlayer(estado)
        (FuturoX,FuturoY) = actionToPoint(playerObj,accion,self.modelo)
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

        # print "Cordinates ",(FuturoX,FuturoY)
        # print "p1 - p3 ",self.p1," ",self.p3
        # print "Distancia bordes "
        # print "DistC1 ",distC1
        # print "DistC2 ",distC2
        # print "DistC3 ",distC3
        # print "DistC4 ",distC4

        minBor = min(distC1,distC2,distC3,distC4)
        # print "Distancia a Borde mas cercano ",minBor

        self.vector.add("minDistBord",1/(minBor+0.1))

        return self.vector

class comiditas(Feature):
    def __init__(self,modelo):
        Feature.__init__(self,modelo)
        self.descriptor = ["minDistFood","minDistBord","distObs","bias"]
    def getValue(self,estado,accion):
        self.vector = bordAndDistFeature(self.modelo).getValue(estado,accion)
        playerObj = getPlayer(estado)
        mindist = 9999
        (FuturoX,FuturoY) = actionToPoint(playerObj,accion,self.modelo)

        for obj in estado:
            if obj != playerObj and obj.isComida:
                Xaux=obj.x
                Yaux=obj.y
                mindist=min(mindist,distance(FuturoX,FuturoY,Xaux,Yaux))
        self.vector.add("minDistFood",1/(mindist+0.1))
        return self.vector

class perseFeature(Feature):

    def __init__(self,modelo):
        Feature.__init__(self,modelo)
        self.descriptor = ["perseDist","minDistFood","minDistBord","distObs","bias"]
    def getValue(self,estado,accion):
        self.vector = comiditas(self.modelo).getValue(estado,accion)
        playerObj = getPlayer(estado)
        mindist = 9999
        (FuturoX,FuturoY) = actionToPoint(playerObj,accion,self.modelo)
        #bla
        for obj in estado:
            if obj != playerObj and obj.isComida:
                Xaux=obj.x
                Yaux=obj.y
                mindist=min(mindist,distance(FuturoX,FuturoY,Xaux,Yaux))
        self.vector.add("perseDist",1/(mindist+0.1))
        return self.vector