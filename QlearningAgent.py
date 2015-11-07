__author__ = 'aferral'

import random
import math
class AproximateQAgent:

    def __init__(self,juego):
        self.weights = [10]
        self.juego = juego
        self.discount = 1
        #Parametro de aprendizaje
        self.alpha = 0.5

        #Parametro de exploracion
        self.epsilon =0

    def getWeights(self):
        return self.weights


    def getQvalue(self,estado,accion):
       # print "El feature es ",self.juego.getFeatures(estado,accion)
       # print "Los pesos son ",self.weights
       # print "El resultado es ",self.juego.getFeatures(estado,accion)*self.weights
        #print "lllllllllllllllllllllllllllll",accion
        print("wighttt"),self.weights
        print "lllllllllllllllllllllllllllll",self.juego.getFeatures(estado,accion)
        print("uuuuu"),self.juego.getFeatures(estado,accion)*self.weights
        return self.juego.getFeatures(estado,accion)*self.weights

    def getMaxQValue(self,estado):
        actions = self.juego.legalActions()
        m = -9999
        #print("uuuuuuuu"),actions
        for action in actions:
            qval = self.getQvalue(estado,action)
            m = max(m,qval)
            #print"9999999999"
        if len(actions) == 0:
            #print("zzzzzzzzzzzzzzz")
            return 0
        return m

    def update(self,estado,accion,proxState,reward):
        #print "mmmm", reward

        sample = reward + self.discount * self.getMaxQValue(proxState)
        diff = sample - self.getQvalue(estado,accion)
        #print "diff", diff

        for inde,feat in enumerate(self.juego.getFeatures(estado,accion)):
            #print "Analizando feature ",inde
            val = self.juego.getFeatures(estado,accion)[inde]
            self.weights[inde] = self.weights[inde] + self.alpha*diff*val


    def getBestAction(self,estado):
        #falta la variable estado
        actions = self.juego.legalActions()
        action = None
        #print("hhhhhhhhhh"),actions
        if len(actions) == 0:
            return action
        if (random.random() < self.epsilon):
            return random.choice(actions)
        else:
            return self.computeActionQvalue(estado)

    def computeActionQvalue(self,estado):
        actions = self.juego.legalActions()
        m = (-9999999999999,0)
        #print("rrrrrrrrrrrr"),actions
        for action in actions:
            #print ("accion"),action*180/math.pi
            qval = self.getQvalue(estado,action)
            #print "QQ", qval,action*180/math.pi
            if m[0] < qval:
                m = (qval,action)
        if len(actions) == 0:
            return 0

        #print("DAAAAAAAAAAAAAAAA"),m
        return m[1]
