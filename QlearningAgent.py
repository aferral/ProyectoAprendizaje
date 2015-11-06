__author__ = 'aferral'

import random
class AproximateQAgent:

    def __init__(self,juego):
        #notar que weight puede tener más dimensiones
        self.weights = None
        self.juego = juego
        self.discount = 1
        #Parametro de aprendizaje
        self.alpha = 0.5

        #Parametro de exploracion
        self.epsilon = 0.2

    def getWeights(self):
        return self.weights


    def getQvalue(self,estado,accion):
        self.juego.getFeatures()*self.weights

    def getMaxQValue(self,estado):
        actions = self.juego.legalActions(estado)
        m = -9999
        for action in actions:
            qval = self.getMaxQValue(estado,action)
            m = max(m,qval)
        if len(action) == 0:
            return 0
        return m

    def update(self,estado,accion,proxState,reward):
        sample = reward + self.discount * self.getMaxQValue(proxState)
        diff = sample - self.getQvalue(estado,accion)

        for feat in self.juego.getFeatures(estado,accion):
            val = self.juego.getFeatures(estado,accion)[feat]
            self.weights[feat] = self.weights[feat] + self.alpha*diff*val


    def getBestAction(self,estado):
        actions = self.juego.legalActions()
        action = None
        if len(actions) == 0:
            return action
        if (random.random() < self.epsilon):
            return random.choice(actions)
        else:
            return self.computeActionQvalue(estado)

    def computeActionQvalue(self,estado):
        actions = self.juego.legalActions(estado)
        m = (-9999,0)
        for action in actions:
            qval = self.getMaxQValue(estado,action)
            if m[0] < qval:
                m = (qval,action)
        if len(action) == 0:
            return 0
        return m[1]
