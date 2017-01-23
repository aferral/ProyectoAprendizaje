import sys
from CustomVector import VectorCustom
from Neuron import MLP_NeuralNetwork
import Neuron

__author__ = 'aferral'

import random
import math


class AbstractQAgent:
    def __init__(self):

        self.aprendizaje = True
        self.weights = VectorCustom()

        self.inputLen = 0
        self.juego = None

        self.discount = 0.1
        #Parametro de aprendizaje
        self.alpha = 0.1

        #Parametro de exploracion
        self.epsilon =0.4


    def configure(self,juego,inputLen):
        self.inputLen = inputLen
        self.juego = juego

    def setWeight(self,planner):
        print planner.weights
        for elem in planner.weights.vals:
            self.weights[elem] = planner.weights.vals[elem]

        self.setEpsilon(0)
        self.endLearning()

    def randomWeight(self):
        temp = VectorCustom()
        for val in self.weights.vals:
            temp.add(val,random.random())
        self.weights = temp
    def setEpsilon(self,val):
        self.epsilon = val
    def endLearning(self):
        self.alpha = 0
        self.aprendizaje = False
    def getWeights(self):
        return self.weights

    def getMaxQValue(self,estado):
        #print ""
        actions = self.juego.legalActions(estado)
        m = -sys.maxint
        for action in actions:
            qval = self.getQvalue(estado,action)

            #print "Action ",action
            #print " Valor ",qval
            m = max(m,qval)
        if len(actions) == 0:
            return 0
        #print ""
        return m

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

    # IMPLEMENTACION NECESITA EDITAR ESTAS FUNCIONES

    def getQvalue(self,estado,accion):
        raise NotImplemented
    def update(self,estado,accion,proxState,reward):
        raise NotImplemented

"""
Esta clase requiere una representacion de estado en features de valor real
luego mediante una combinacion lineal de estas aproximara la funcion Q(s,a)
"""
class AproximateQAgent(AbstractQAgent):

    def configure(self,juego,inputLen):
        AbstractQAgent.configure(self,juego,inputLen)

        for key in juego.featFun.descriptor:
            self.weights[key] = 0


    def getQvalue(self,estado,accion):

        # print "Action ",accion
        # print "Weight",self.weights
        # print "ValFeature ",self.juego.getFeatures(estado,accion)
        # print "Res",self.juego.getFeatures(estado,accion)*self.weights
        # print "//////////////////////////////////////////////////"

        return self.juego.getFeatures(estado,accion)*self.weights

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
        for feature in valFeature.vals:
            val = valFeature[feature]
            # print "Valor de refuerzo ",val
            # print ""
            self.weights[feature] = self.weights[feature] + self.alpha*diff*val
        # print "------------------saliendo update -----------------------"
        # print " "

"""
Esta clase toma otra vez las features, para y arma un red neuronal de una hiden layer para aproximar
Q(s,a) la forma de actualizacion esta dada por
Q(st,a) = rew + gamma*[ max(a{t+1}) Q(s{t+1}, a{t+1})] que sera el target o valor real
Y el valor que estimo anteriormente la red neuronal
"""
class NeuronalQAgentOnline(AbstractQAgent):

    def __init__(self):
        AbstractQAgent.__init__(self)
        self.network = None
        self.bolsa = []
        self.maxContains = 1000

    def setWeight(self,planner):
        #Seteo la red neuronal desde los episodios que guardo
        print planner.weights

        self.bolsa = planner.bolsa

        #self.network = MLP_NeuralNetwork(self.inputLen-1+1, 5, 1, iterations = 1000, learning_rate = 0.5, momentum = 0.01, rate_decay = 0.01)
        #self.network.train(self.bolsa)

        self.network = planner.network

        self.setEpsilon(0)
        self.endLearning()

    def configure(self,juego,inputLen):
        AbstractQAgent.configure(self,juego,inputLen)
        #lerng 0.5 momento 0.01
        self.network = MLP_NeuralNetwork(self.inputLen-1+1, 3, 1, iterations = 1, learning_rate = 0.5, momentum = 0.01, rate_decay = 0.01)

    def formatInputActions(self,estado,accion):
        vector = []
        #Procesa feature como lista
        representacion = self.juego.getFeatures(estado,accion)
        #print representacion
        for feature in representacion.vals:
            if feature == "bias":
                continue
            val = representacion.vals[feature]
            vector.append(val)
        vector.append(accion)
        #print (vector)
        return vector




    def getQvalue(self,estado,accion):

        # print "Action ",accion
        # print "Weight",self.weights
        # print "ValFeature ",self.juego.getFeatures(estado,accion)
        # print "Res",self.juego.getFeatures(estado,accion)*self.weights
        # print "//////////////////////////////////////////////////"
        val = self.network.predict([self.formatInputActions(estado,accion)])[0][0]
        return val

    def update(self,estado,accion,proxState,reward):

        if (not self.aprendizaje):
            return
        """ Esto no funciono
        (s1,action,s2,reward) = (estado,accion,proxState,reward)
        target = reward + self.discount * self.getMaxQValue(s2)
        target = Neuron.tanh(target)

        inputs = self.formatInputActions(s1,action)

        #Actualizo el valor
        self.network.feedForward(inputs)
        self.network.backPropagate([target])

        #Realizo algunas cuantas iteraciones para actualizar otros valores
        interval = min(len(self.bolsa),10)
        for i in range(interval):
            index = random.randint(0,len(self.bolsa)-1)
            #print len(self.bolsa),index
            (s1,action,s2,reward) = self.bolsa[index]
            target = reward + self.discount * self.getMaxQValue(s2)
            target = Neuron.tanh(target)

            inputs = self.formatInputActions(s1,action)

            self.network.feedForward(inputs)
            self.network.backPropagate([target])

        self.bolsa.append((s1,action,s2,reward))
        """
        target = reward + self.discount * self.getMaxQValue(proxState)
        target = Neuron.tanh(target)
        self.bolsa.append([self.formatInputActions(estado,accion),[target] ])

        #self.network.train([[self.formatInputActions(estado,accion),[target]] ])
        self.network.train(self.bolsa)
