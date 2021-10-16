import turtle
import tkinter
import time
from queue import PriorityQueue

#Posiciones del laberinto
pos1 = -429,375
pos2 = -215,375
pos3 = -1,375
pos4 = 213,375
pos5 = 427,375
pos6 = -429,125
pos7 = -215,125
pos8 = -1,125
pos9 = 213,125
pos10 = 427,125
pos11 = -429,-125
pos12 = -215,-125
pos13 = -1,-125
pos14 = 213,-125
pos15 = 427,-125
pos16 = -429,-375
pos17 = -215,-375
pos18 = -1,-375
pos19 = 213,-375
pos20 = 427,-375

arbol = []
costos = PriorityQueue()

#Clase arbol
class Arbol:
    def __init__(self, elemento):
        self.hijos = []
        self.elemento = elemento

def agregarElemento(arbol, elemento, elementoPadre):
    subarbol = buscarSubarbol(arbol, elementoPadre)
    subarbol.hijos.append(Arbol(elemento))

def buscarSubarbol(arbol, elemento):
    if arbol.elemento == elemento:
        return arbol
    for subarbol in arbol.hijos:
        arbolBuscado = buscarSubarbol(subarbol, elemento)
        if (arbolBuscado != None):
            return arbolBuscado
    return None   


def buscarPadre(arbol, hijo, padre):
    if arbol.elemento == hijo:
        return padre
    padre=arbol
    for subarbol in arbol.hijos:
        arbolBuscado = buscarPadre(subarbol, hijo, padre)
        if (arbolBuscado != None):
            return arbolBuscado
    return None

def ancestros(arbol, elemento):
    if elemento == None:
        return recorrido
    else:
        nodo = buscarPadre(arbol,elemento,None)
        if nodo == None:
            return recorrido
        recorrido.append(nodo.elemento)
        ancestros(arbol, nodo.elemento)

#Matriz del laberinto
#---------------
#0 Casilla vacia
#1 Mononoke
#2 Kodama
#3 Venado
#4 Rey
#5 Pared

tablero = [[1,4,0,0,0],
           [0,5,0,0,0],
           [0,5,0,5,0],
           [3,2,0,5,0]]

posiciones = [[pos1,pos2,pos3,pos4,pos5],
              [pos6,pos7,pos8,pos9,pos10],
              [pos11,pos12,pos13,pos14,pos15],
              [pos16,pos17,pos18,pos19,pos20]]

kodamas = []
arboles = []
yakult = turtle.Turtle()
camino = []
recorrido = []

#Fondo cargado con la imagen base del laberinto
turtle.title("Laberinto de Mononoke")
screen = turtle.Screen()
screen.setup(1085,1000)
screen.bgpic('fondo2.gif')

# Mover

def mover(tortuga):
    for i in range(len(camino)-1):
        tortuga.goto(camino[len(camino)-1-i])

#ia mononoke
#cambie todo por tablero
def iaCosto(mononoke,x,y,contador):

    costo = 0
    if contador == 0:
            tree = Arbol((costo,posiciones[x][y]))  
            
    if tablero[x][y] == 4:
        #padre = buscarPadre(arbol, elemento)
        #elemento = buscarSubarbol(tree,posiciones[x][y])
        
        #mover(mononoke)
        #Imprimir matriz recorrido
        tkinter.messagebox.showinfo(message="ENCONTRÓ LA META", title="FIN")

    #abajo  
    if tablero[x+1][y] != 5 and 4 > x+1:
        #movimiento posible, agregue a la cola
        #analizar
        """
        if posiciones[x+1][y] == (0 or 1 or 3 or 4):
            costo += 1
        if posiciones[x+1][y] == 2:
            costo += 3    
        """
        if tablero[x+1][y] == 2:
            costo+=2
        else:
            costo+1
        #analizar
        """    
        agregarElemento(tree,(costo,posiciones[x+1][y]),posiciones[x][y])
        """

    #derecha            
    if tablero[x][y+1] != 5 and 4 > y+1:
        #movimiento posible, agregue a la cola
        if tablero[x-1][y+1] == 2:
            costo+=2
        else:
            costo+1   

    #arriba    
    if tablero[x-1][y] != 5 and x-1 > 0:
        #movimiento posible, agregue a la cola
        if tablero[x-1][y] == 2:
            costo+=2
        else:
            costo+1 

    #izquierda
    if tablero[x][y-1] != 5 and y-1 > 0:
        #movimiento posible, agregue a la cola
        if tablero[x][y-1] == 2:
            costo+=2
        else:
            costo+1

    #Ejecutar funcion de costo

#Dibujar mononoke

def dibujarMononoke():

    for i in range (len(tablero)):
        for j in range (len(tablero[i])):
            if tablero[i][j] == 1:
                mononoke = turtle.Turtle()
                image = "mononoke2.gif"
                screen.addshape(image)
                mononoke.shape(image)
                mononoke.ht()
                mononoke.penup()
                mononoke.setposition(posiciones[i][j])
                mononoke.st()
                iaCosto(mononoke,i,j,0)

def dibujarKodama():

    for i in range (len(tablero)):
        for j in range(len(tablero[i])):
            if tablero[i][j] == 2:
                kodamas.append(turtle.Turtle())
                imagekodama = "kodamas2.gif"
                if len(kodamas) == 1:
                    screen.addshape(imagekodama)
                kodamas[len(kodamas)-1].shape(imagekodama)
                kodamas[len(kodamas)-1].ht()
                kodamas[len(kodamas)-1].penup()
                kodamas[len(kodamas)-1].setposition(posiciones[i][j])
                kodamas[len(kodamas)-1].st()

def dibujarYakult():

    for i in range (len(tablero)):
        for j in range (len(tablero[i])):
            if tablero[i][j] == 3:
                image = "yakult2.gif"
                screen.addshape(image)
                yakult.shape(image)
                yakult.ht()
                yakult.penup()
                yakult.setposition(posiciones[i][j])
                yakult.st() 

def dibujarEspiritu():

    for i in range (len(tablero)):
        for j in range (len(tablero[i])):
            if tablero[i][j] == 4:
                espiritu = turtle.Turtle()
                image = "espiritu2.gif"
                screen.addshape(image)
                espiritu.shape(image)
                espiritu.ht()
                espiritu.penup()
                espiritu.setposition(posiciones[i][j])
                espiritu.st()                       



def dibujarArbol():

    for i in range (len(tablero)):
        for j in range (len(tablero[i])):
            if tablero[i][j] == 5:
                arboles.append(turtle.Turtle())
                if len(arboles) == 1:
                    imagearbol = "arbol2.gif"
                    screen.addshape(imagearbol)
                arboles[len(arboles)-1].shape(imagearbol)
                arboles[len(arboles)-1].ht()
                arboles[len(arboles)-1].penup()
                arboles[len(arboles)-1].setposition(posiciones[i][j])
                arboles[len(arboles)-1].st()            

"""dibujarKodama() 
dibujarArbol()  
dibujarYakult() 
dibujarEspiritu()
dibujarMononoke()"""

abuela = "Jacqueline Gurney"
homero= "Homero Simpson"
marge = "Marge Bouvier"
patty = "Patty Bouvier"
selma = "Selma Bouvier"
bart = "Bart Simpson"
lisa = "Lisa Simpson"
maggie = "Maggie Simpson"
ling = "Ling Bouvier"
arbol = Arbol(abuela)
agregarElemento(arbol, patty, abuela)
agregarElemento(arbol, selma, abuela)
agregarElemento(arbol, ling, selma)
agregarElemento(arbol, marge, abuela)
agregarElemento(arbol, bart, marge)
agregarElemento(arbol, lisa, marge)
agregarElemento(arbol, maggie, marge)

"""""
print((buscarPadre(arbol,bart,None)))
print((buscarPadre(arbol,marge,None)))
print((buscarPadre(arbol,abuela,None)))
"""""

ancestros(arbol,ling)
for i in range (len(recorrido)):
    print(recorrido[i])
turtle.done()
