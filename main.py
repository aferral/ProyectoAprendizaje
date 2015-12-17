import copy
from Model import JuegoModelo
import sys
import argparse
import pygame
from utils import *
__author__ = 'aferral'

plotPosible = True

try:
    import matplotlib.pyplot as plt
except Exception,e :
    print "Error al conseguir matplotlib.pyplot no ploteare solo imprimire"
    plotPosible = False

#Generar modo debug con grideo

#Fabrica de juegos
def fabricaJuego(args):

    nuevoJuego = JuegoModelo()

    nuevoJuego.generateRandomObs(args.nEnemies)
    nuevoJuego.generateRandomFoods(args.Food)
    nuevoJuego.generateRandomPersecutor(args.persecutoresEnemies)

    nuevoJuego.setFeatureArg(args.feature)

    if args.training:
        trainModel(nuevoJuego,constTime,args.training)
    return nuevoJuego


#Def functiones de entrenamiento y prueba

def trainModel(juego,constTime,iterations):
    print "Starting training of ",iterations
    print "Weights ",juego.planner.weights
    juego.planner.setEpsilon(0.8)
    for i in range(iterations):
        juego.updateGame(constTime)
    juego.planner.setEpsilon(0)
    print "Traing has ended ",juego.planner.weights

    return juego.planner.weights

def experiment(constTime,args):
    #Genera lista de numero de iteraciones de entrenamiento
    nTrain = [0, 1, 10, 20, 50,80,100,200,300,400,500,600,700,800,900,1000]
    allTheScores = []

    #Cuanto debe durar el juego en que se prueba (iteraciones)
    iteracionesTest = 100

    #Cuantas veces se vuelve a probar un par (nTrain,ItearcionTest) para sacar el valro promedio
    repe = 10

    for iteracionTrain in nTrain:
        #Entrena con iteracionTrain entrenamiento dentro de fabrica
        print "Comienzan experimentos con iteracionesTrain ",iteracionTrain
        argTrain= args
        argTrain.training = iteracionTrain
        modeloPruebas = fabricaJuego(argTrain)

        weightTrained = modeloPruebas.planner.weights
        argNoTrain = args
        argNoTrain.training = 0

        averageScore = 0
        for i in range(repe):
            nuevoTest = fabricaJuego(argNoTrain)
            nuevoTest.setWeight(weightTrained)
            averageScore += testModel(nuevoTest,constTime,iteracionesTest)
        averageScore /= repe
        print "Acabo de terminar de probar el modelo con ",iteracionTrain," iteraciones "," con un score de ",averageScore
        allTheScores.append(averageScore)
    #Plotea que las iteracionse de entrenamiento y el scorePromedio obtenido

    if (plotPosible):
        plt.plot(nTrain,allTheScores,'*--')
        plt.show()

    print "Resultados "
    print nTrain
    print allTheScores


def testModel(juego,constTime,iterations):
    print "Starting test of ",iterations
    print "Weights ",juego.planner.weights
    decim = 1 + iterations / 100.0
    for i in range(iterations):
        if i % decim == 0:
            print "Test en ",(i*100.0/iterations)
        juego.updateGame(constTime)
    print "Traing has ended el score es ",juego.score
    return juego.score
    pass

def validateModel(self):
    pass


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

    def movePlayer(self,deltaAng):
        playerObj = getPlayer(self.juegomodelo.estadoActual)
        playerObj.moveAngle(deltaAng)
        pass

    def loop(self):
        difAngul = 0
        while not self.done:
            # Clear the screen
            self.screen.fill(WHITE)

            if self.modoStep:
                raw_input()
                #Aca dibujar mapa de features
                self.drawQvalues()

            control = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == KEYUP:
                    difAngul = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print "Izq"
                        difAngul = 0.1
                    if event.key == pygame.K_RIGHT:
                        print "Derecha"
                        difAngul = -0.1
                    if event.key == pygame.K_UP:
                        print "Arriba"
                    if event.key == pygame.K_DOWN:
                        print "Down"
                        pygame.display.flip()
            self.movePlayer(difAngul)
            listaObjetos = self.juegomodelo.estadoActual
            self.juegomodelo.updateGame(constTime)
            for elem in listaObjetos:
                elem.setDraw(self.screen)
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
parser.add_argument(dest="persecutoresEnemies", type=int,help="Cuantos meteoros colocar", default=3, nargs='?')

parser.add_argument(dest='feature', type=str,help="justDist, borderDist, foodDist", default='foodDist', nargs='?')
parser.add_argument(dest="Food", type=int,help="Cuantos meteoros colocar", default=40, nargs='?')

parser.add_argument(dest='training',help="0 No pre training 1 pre Training", default=0, nargs='?')
parser.add_argument(dest='ExpOrRun',help="0 experiment,  1 visualGame, 2 jugar desde 0", default=2, nargs='?')

args = parser.parse_args()
print args
#Setear el juego, modelo


#Crea modelo segun parametros (puede ser necesario entrenarlo)


#Debe ser necesario crear pesos aleatorios


#SI es 1 se juega con modo normal visual
if args.ExpOrRun == 1:
    modeloReal = fabricaJuego(args)
    vista = JuegoVisual(modeloReal)
    vista.loop()

elif  args.ExpOrRun == 2:
    args.training = 0
    modeloReal = fabricaJuego(args)
    modeloReal.planner.setEpsilon(0.2)
    modeloReal.planner.alpha = 0.4
    vista = JuegoVisual(modeloReal)
    vista.loop()
else: #De lo contrario se coloca en modo experimento que hace sin interfaz grafica
    experiment(constTime,args)







