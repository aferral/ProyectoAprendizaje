__author__ = 'aferral'
import math
def d(obj1,obj2):
    return math.sqrt(math.pow((obj1.x-obj2.x),2)+math.pow((obj1.y-obj2.y),2))
def distance(x1,y1,x2,y2):
    return math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))

def getAngle(obj1,obj2):
    return math.atan2(obj2.y,obj2.x)-math.atan2(obj1.y,obj1.x)

def actionToPoint(obj,action):
    deltaX= obj.velModulo*math.cos(action)*4
    deltaY= obj.velModulo*math.sin(action)*4
    FuturoX=obj.x + deltaX
    FuturoY=obj.y + deltaY
    return (FuturoX,FuturoY)
def getPlayer(estado):
    return estado[0]