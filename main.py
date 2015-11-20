import copy
from Model import JuegoModelo
import sys
import argparse
import pygame
from utils import *
__author__ = 'aferral'


#Generar modo debug con grideo

#Iteraciones modo antes de probar


#Todo Separar el fin de juego del juego, si se acaba el juego tirar el main dneuvo (guardando weights(


#Todo formalizar la cosa de las features nose hacer una clase o algo, ademas de una buena forma de
#Inicializar vectores peso

# Define some colors
WHITE = (255, 255, 255)

fps = 20
constTime = 20/1000.0


from pygame.locals import *
class JuegoVisual:
    def __init__(self,juegomodelo):

        #Variable prueba
        self.modoStep = False

        self.done = False
        self.juegomodelo = juegomodelo

        pygame.init()
        self.screen = pygame.display.set_mode(
            [self.juegomodelo.dim[0], self.juegomodelo.dim[1]],HWSURFACE|DOUBLEBUF|RESIZABLE)

        for elem in self.juegomodelo.listaObstaculos:
            elem.setDraw(self.screen)
        self.clock = pygame.time.Clock()

    def drawBorde(self):
        pygame.draw.line(self.screen, (0,255,0), self.juegomodelo.p1, self.juegomodelo.p2)
        pygame.draw.line(self.screen, (0,255,0), self.juegomodelo.p2, self.juegomodelo.p3)
        pygame.draw.line(self.screen, (0,255,0), self.juegomodelo.p3, self.juegomodelo.p4)
        pygame.draw.line(self.screen, (0,255,0), self.juegomodelo.p4, self.juegomodelo.p1)
        pass

    """ Importante esta es una visualizacion solamente de los Qvalues
        respecto a la posicion del jugador manteniendo todos los demas
        parametros constantes. Ademas puede tener probleams de visualizacion
        respecto a las funciones discontinuas ya que no puede considerar
        todos lso punts que se implemeten en las distintas
        features usarla con cuidado.
    """
    def drawQvalues(self):

        #Discretizar el grid en cuantos pasos


        h = 8
        listaPoints = [0 for j in range(h*h)]

        matrix = [[copy.deepcopy(self.juegomodelo.estadoActual) for j in range(h)] for i in range(h)]

        import time
        startTime = time.time()
        stepX = (self.juegomodelo.dim[0]-10) * 1.0 / h
        stepY = (self.juegomodelo.dim[1]-10) * 1.0 / h


        listaColores = linear_gradient(20)

        for index in range(h*h):
                i = index / h
                j = index % h
                (xcord,ycord) = (stepX * i,stepY*j)

                estado = matrix[i][j]
                jug = getPlayer(estado)
                jug.teleport((xcord,ycord))
                valPoint = self.juegomodelo.planner.getMaxQValue(estado)
                listaPoints[i*h+j] = valPoint

        minval = min(listaPoints)
        maxval = max(listaPoints)
        for index,value in enumerate(listaPoints):
            i = index / h
            j = index % h
            (xcord,ycord) = (stepX * i,stepY*j)
            color = calculaColor(minval,maxval,value,listaColores)
            pygame.draw.rect(self.screen,color,
                                  (int(xcord)-stepX*0.5,int(ycord)-stepY*0.5,int(xcord)+stepX*0.5,int(ycord)+stepY*0.5)
                                  ,0)
        print "Tomo ",time.time()-startTime
        far = pygame.font.SysFont("comicsansms", 12)
        text = far.render("Weight "+str(self.juegomodelo.planner.weights), True, (0, 0, 0))
        self.screen.blit(text, (20, 20))
        pass

    def loop(self):

        while not self.done:
            # Clear the screen
            self.screen.fill(WHITE)

            if self.modoStep:
                raw_input()
                #Aca dibujar mapa de features
                self.drawQvalues()

            control = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print "Izq"
                        self.juegomodelo.listaObstaculos[control].changeSpeed((-1,0))

                    if event.key == pygame.K_RIGHT:
                        print "Derecha"
                        self.juegomodelo.listaObstaculos[control].changeSpeed((1,0))
                    if event.key == pygame.K_UP:
                        print "Arriba"
                        self.juegomodelo.listaObstaculos[control].changeSpeed((0,-1))
                    if event.key == pygame.K_DOWN:
                        print "Down"
                        self.juegomodelo.listaObstaculos[control].changeSpeed((0,1))

                        pygame.display.flip()

            listaObjetos = self.juegomodelo.listaObstaculos
            self.juegomodelo.updateGame(constTime)
            for elem in listaObjetos:
                elem.draw()

            #Elementos auxiliares
            for point in self.juegomodelo.superestados:
                #print"pppp1",point
                if point == None or point == 0:
                    continue
                #print "Punto sigiente ",point
                #print"pppp",point
                pygame.draw.circle(self.screen,(255,0,0),(int(point[0]),int(point[1])),2,1)

            self.drawBorde()
            # Limit to X frames per second
            self.clock.tick(fps)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        pygame.quit()


parser = argparse.ArgumentParser()
parser.add_argument(dest="nEnemies", type=int,help="Cuantos meteoros colocar", default=7, nargs='?')
parser.add_argument(dest="persecutoresEnemies", type=int,help="Cuantos meteoros colocar", default=1, nargs='?')

parser.add_argument(dest='feature', type=str,help="justDist, borderDist, foodDist", default='foodDist', nargs='?')
parser.add_argument(dest="Food", type=int,help="Cuantos meteoros colocar", default=40, nargs='?')

parser.add_argument(dest='training',help="0 No pre training 1 pre Training", default=1000, nargs='?')
parser.add_argument(dest='testOrVisual',help="0 test 1 visualGame", default=0, nargs='?')

args = parser.parse_args()
print args
#Setear el juego, modelo

modeloReal = JuegoModelo()
modeloTraining = JuegoModelo()

modeloTraining.generateRandomObs(args.nEnemies)
modeloTraining.generateRandomFoods(args.Food)
modeloReal.generateRandomObs(args.nEnemies)
modeloReal.generateRandomFoods(args.Food)
modeloReal.generateRandomPersecutor(args.persecutoresEnemies)


modeloTraining.setFeatureArg(args.feature)
modeloReal.setFeatureArg(args.feature)

if args.training:
    w = modeloTraining.trainModel(constTime,args.training)

if args.testOrVisual == 1:
    modeloReal.setWeight(w)
    vista = JuegoVisual(modeloReal)
    vista.loop()
else:
    modeloReal.setWeight(w)
    modeloReal.testModel(constTime,1000)

    print "Ahora con pesos aleatorios "
    modeloReal = JuegoModelo()
    modeloReal.generateRandomObs(args.nEnemies)
    modeloReal.generateRandomPersecutor(args.persecutoresEnemies)
    modeloReal.generateRandomFoods(args.Food)
    modeloReal.setFeatureArg(args.feature)

    modeloReal.planner.randomWeight()
    modeloReal.testModel(constTime,1000)




