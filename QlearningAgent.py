import sys
from CustomVector import VectorCustom

__author__ = 'aferral'

import random
import math
class AproximateQAgent:

    def __init__(self,juego):
        self.weights = VectorCustom()
        self.weights.add(0)
        self.juego = juego
        self.discount = 0.3
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
        # print "Weight",self.weights
        # print "Features ",self.juego.getFeatures(estado,accion)
        # print ""
        # print("uuuuu"),self.juego.getFeatures(estado,accion)*self.weights
        return self.juego.getFeatures(estado,accion)*self.weights

    def getMaxQValue(self,estado):
        actions = self.juego.legalActions()
        m = -sys.maxint
        #print("uuuuuuuu"),actions
        for action in actions:
            qval = self.getQvalue(estado,action)
            print "Action ",action," valor ",qval
            print ""
            m = max(m,qval)
            #print"9999999999"
        if len(actions) == 0:
            #print("zzzzzzzzzzzzzzz")
            return 0
        return m

    def update(self,estado,accion,proxState,reward):


        sample = reward + self.discount * self.getMaxQValue(proxState)
        estimacion = self.getQvalue(estado,accion)
        diff = sample - estimacion
        print "Reward", reward
        print "diff", diff
        print "Valor sample ",sample
        print "Valor estimacion ",estimacion

        for inde,feat in enumerate(self.juego.getFeatures(estado,accion)):
            val = self.juego.getFeatures(estado,accion)[inde]
            print "Valor de refuerzo ",val
            print ""
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
