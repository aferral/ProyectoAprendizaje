__author__ = 'aferral'
import math
def d(obj1,obj2):
    return math.sqrt(math.pow((obj1.x-obj2.x),2)+math.pow((obj1.y-obj2.y),2))
def distance(x1,y1,x2,y2):
    return math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))

def getAngle(obj1,obj2):
    return math.atan2(obj2.y,obj2.x)-math.atan2(obj1.y,obj1.x)

def actionToPoint(obj,action, modelo):

    deltaX= obj.velModulo*math.cos(action)*4
    deltaY= obj.velModulo*math.sin(action)*4
    if modelo.traspasarPared ==False:
        FuturoX=obj.x + deltaX
        FuturoY=obj.y + deltaY
    else:
        FuturoX=obj.x + deltaX
        FuturoY=obj.y + deltaY
        for i in range(4):
            pared=modelo.borders1[i]
            margin=pared
            # bla = [self.borders[2],self.borders[3],self.borders[0],self.borders[1]]
            # pared=bla[i]
            if i == 0 and (pared-(FuturoX)) > 0:
               # print "Choque en 0"
                FuturoX = FuturoX + modelo.borders1[1]
            if i == 1 and ((FuturoX)- pared) > 0:
               # print "Choque en 1"
                FuturoX = FuturoX - pared
             #   obj.velX *= -1
            if i == 2 and ((FuturoY)- pared) > 0:
              #  print "Choque en 2"
                FuturoY = FuturoY - margin
              #  obj.velY *= -1
            if i == 3 and (pared-(FuturoY)) > 0:
              #  print "Choque en 3"
                FuturoY = FuturoY + modelo.borders1[2]
               # obj.velY *= -1
        # exit(1)
        pass

    return (FuturoX,FuturoY)
def getPlayer(estado):
    return estado[0]



#Cosas para visualizacion


def linear_gradient(n=10):

  # Starting and ending colors in RGB form
  s = (0,0,255)
  f = (255,0,0)
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    RGB_list.append(curr_vector)

  return RGB_list

def calculaColor(minval,maxval,value,lista):
    intervalo = (maxval-minval)*1.0/(len(lista))
    bin = int(math.floor((value-minval-1) / intervalo))
    return lista[bin]