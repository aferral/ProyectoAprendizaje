import sys
from CustomVector import VectorCustom

__author__ = 'aferral'

import random
import math
class AproximateQAgent:

    def __init__(self,juego):
        self.weights = VectorCustom()

        self.juego = juego
        self.discount = 0.8
        #Parametro de aprendizaje
        self.alpha = 1

        #Parametro de exploracion
        self.epsilon =0.4

    def setEpsilon(self,val):
        self.epsilon = val
    def endLearning(self):
        self.alpha = 0
    def getWeights(self):
        return self.weights


    def getQvalue(self,estado,accion):

        # print "Action ",accion
        # print "Weight",self.weights
        # print "ValFeature ",self.juego.getFeatures(estado,accion)
        # print "Res",self.juego.getFeatures(estado,accion)*self.weights
        # print "//////////////////////////////////////////////////"

        return self.juego.getFeatures(estado,accion)*self.weights

    def getMaxQValue(self,estado):
        actions = self.juego.legalActions(estado)
        m = -sys.maxint
        for action in actions:
            qval = self.getQvalue(estado,action)
            # print "Action ",action," valor ",qval

            m = max(m,qval)
        if len(actions) == 0:
            return 0
        return m

    #SARSA
    def update(self,estado,accion,proxState,reward):


        sample = reward + self.discount * self.getMaxQValue(proxState)
        estimacion = self.getQvalue(estado,accion)
        diff = sample - estimacion
        valFeature = self.juego.getFeatures(estado,accion)

        # print " "
        # print "------------------En funcion update -----------------------"
        # print "Reward", reward
        # print "diff", diff
        # print "Valor sample ",sample
        # print "Valor estimacion ",estimacion
        # print "Valor feature en estado ",valFeature

        for inde,feat in enumerate(valFeature):
            val = valFeature[inde]
            # print "Valor de refuerzo ",val
            # print ""
            self.weights[inde] = self.weights[inde] + self.alpha*diff*val
        # print "------------------saliendo update -----------------------"
        # print " "

    def getBestAction(self,estado):
        #falta la variable estado
        actions = self.juego.legalActions(estado)
        action = None
        #print("hhhhhhhhhh"),actions
        if len(actions) == 0:
            return action
        if (random.random() < self.epsilon):
            return random.choice(actions)
        else:
            return self.computeActionQvalue(estado)

    def computeActionQvalue(self,estado):
        actions = self.juego.legalActions(estado)
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
        return m[1]
