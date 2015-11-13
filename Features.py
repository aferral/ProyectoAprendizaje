from CustomVector import VectorCustom
from utils import *

__author__ = 'aferral'

class FeatureExtractor:
    def __init__(self,modelo):
        self.p1 = modelo.p1
        self.p2 = modelo.p2
        self.p3 = modelo.p3
        self.p4 = modelo.p4



    def justDistFeature(self,estado,accion):
        playerObj = getPlayer(estado)
        mindist = 9999
        vec = VectorCustom()
        distNextStep = mindist
        (FuturoX,FuturoY) = actionToPoint(playerObj,accion)

        for obj in estado:
            if obj != playerObj and obj.isComida == False:
                Xaux=obj.x
                Yaux=obj.y
                mindist=min(mindist,distance(FuturoX,FuturoY,Xaux,Yaux))

        vec.add(10/(mindist))
        vec.add(1)
        return vec
    def bordAndDistFeature(self,estado,accion):

        playerObj = getPlayer(estado)
        mindist = 9999
        vec = VectorCustom()
        distNextStep = mindist
        (FuturoX,FuturoY) = actionToPoint(playerObj,accion)

        for obj in estado:
            if obj != playerObj and obj.isComida == False:
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

        # print "Cordinates ",(FuturoX,FuturoY)
        # print "p1 - p3 ",self.p1," ",self.p3
        # print "Distancia bordes "
        # print "DistC1 ",distC1
        # print "DistC2 ",distC2
        # print "DistC3 ",distC3
        # print "DistC4 ",distC4

        minBor = min(distC1,distC2,distC3,distC4)
        # print "Distancia a Borde mas cercano ",minBor

        vec.add(3/(minBor+0.1))
        vec.add(10/(mindist))
        vec.add(1)
        return vec

    def comiditas(self,estado,accion):
        vec = self.bordAndDistFeature(estado,accion)
        playerObj = getPlayer(estado)
        mindist = 9999
        (FuturoX,FuturoY) = actionToPoint(playerObj,accion)

        for obj in estado:
            if obj != playerObj and obj.isComida:
                Xaux=obj.x
                Yaux=obj.y
                mindist=min(mindist,distance(FuturoX,FuturoY,Xaux,Yaux))
        vec.add(1/(mindist))
        return vec