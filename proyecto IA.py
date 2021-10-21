from tkinter.constants import NO
import turtle
import tkinter as tk
import time
from queue import PriorityQueue
import sys
contadorglobal = 0
nodosglobal = 1
limiteglobal = 0
xglobal = 0
yglobal = 0
#Coordenadas de los cuadros del laberinto
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

def ancestros(arbol, elemento): #
    if elemento == None:
        return recorrido
    else:
        nodo = buscarPadre(arbol,elemento,None)
        if nodo == None:
            return recorrido
        recorrido.append(nodo.elemento)
        ancestros(arbol, nodo.elemento)

def ejecutarProfundidadPrimero(arbol, funcion):
    funcion(arbol.elemento)
    for hijo in arbol.hijos:
        ejecutarProfundidadPrimero(hijo, funcion)

def printElement(element):
    print(element)


#Matriz del laberinto
#---------------
#0 Casilla vacia
#1 Mononoke
#2 Kodama
#3 Venado
#4 Rey
#5 Pared

tablero = [[1,3,2,2,4],
           [0,5,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0]]


posiciones = [[pos1,pos2,pos3,pos4,pos5],       #Matriz de posiciones que guarda las coordenadas de cada cuadro en el tablero
              [pos6,pos7,pos8,pos9,pos10],
              [pos11,pos12,pos13,pos14,pos15],
              [pos16,pos17,pos18,pos19,pos20]]

kodamas = [] #Array para verificar la cantidad de kodamas y crearlos 
arboles = [] #Array para verificar la cantidad de árboles y crearlos 
yakult = turtle.Turtle() #Yakult definido afuera para borrarlo en caso de que Mononoke se monte
recorrido = [] #Array que guarda el recorrido desde la meta hasta la posición inicial (Yendose por el padre de la meta y sucesivamente)

#Fondo cargado con la imagen base del laberinto (sin ningún elemento)
turtle.title("Laberinto de Mononoke")
screen = turtle.Screen()
screen.setup(1085,1000)
screen.bgpic('fondo2.gif')

# Mover
def mover(tortuga):
        
    for i in range(len(recorrido)):
        x = recorrido[len(recorrido)-1-i][0]
        y = recorrido[len(recorrido)-1-i][1]

        tortuga.goto(posiciones[x][y])
        if tablero[x][y] == 3: #Mononoke se monta en Yakult
            yakult.ht()
            montada = "mononokemontada.gif"
            screen.addshape(montada)
            tortuga.shape(montada)
        if tablero[x][y] == 4: #Mononoke se monta en el espíritu
            meta = "meta.gif"
            screen.addshape(meta)
            tortuga.shape(meta)
    

#ia Mononoke costo
def iaCosto(mononoke,x,y,costo,flag,limite,padre,arbol):
    
    if tablero[x][y] == 4: #Comprueba si la posicion actual es meta
        #Se agrega la posición de meta al array de recorrido
        recorrido.append((x,y,limite,flag))
        #Llama la funcion ancestros 
        ancestros(arbol,(x,y,limite,flag))
        mover(mononoke)
        tk.messagebox.showinfo(message="ENCONTRÓ LA META. COSTO TOTAL = "+ str(costo), title="FIN")
        return None
    
    #Paso por venado
    if tablero[x][y] == 3:
        flag=1     

    #derecha  
    if y+1 <= 4:
        if tablero[x][y+1] != 5:
            #movimiento posible
            if tablero[x][y+1] == 2 and flag==0:
                costos.put((costo+2,limite+1,x,y+1,flag)) #Se agrega una tupla que tiene el costo de la casilla y las posiciones en X & Y
                agregarElemento(arbol,(x,y+1,limite+1,flag),(x,y,limite,padre))
            else:
                costos.put((costo+1,limite+1,x,y+1,flag))
                agregarElemento(arbol,(x,y+1,limite+1,flag),(x,y,limite,padre))

    #abajo  
    if x+1 <= 3:   
        if tablero[x+1][y] != 5:
            #movimiento posible, agregue a la cola
            if tablero[x+1][y] == 2 and flag==0:
                costos.put((costo+2,limite+1,x+1,y,flag)) #Se agrega una tupla que tiene el costo de la casilla y las posiciones en X & Y
                agregarElemento(arbol,(x+1,y,limite+1,flag),(x,y,limite,padre)) #Se agrega un hijo a este arbol, que tendrá como padre la pos actual
            else:
                costos.put((costo+1,limite+1,x+1,y,flag)) #Se agrega una tupla que tiene el costo de la casilla y las posiciones en X & Y  
                agregarElemento(arbol,(x+1,y,limite+1,flag),(x,y,limite,padre))

    #izquierda 
    if y-1 >= 0:
        if tablero[x][y-1] != 5:
            #movimiento posible, agregue a la cola
            if tablero[x][y-1] == 2 and flag==0:
                costos.put((costo+2,limite+1,x,y-1,flag)) #Se agrega una tupla que tiene el costo de la casilla y las posiciones en X & Y
                agregarElemento(arbol,(x,y-1,limite+1,flag),(x,y,limite,padre)) #Se agrega un hijo a este arbol, que tendrá como padre la pos actual
            else:
                costos.put((costo+1,limite+1,x,y-1,flag)) #Se agrega una tupla que tiene el costo de la casilla y las posiciones en X & Y
                agregarElemento(arbol,(x,y-1,limite+1,flag),(x,y,limite,padre)) #Se agrega un hijo a este arbol, que tendrá como padre la pos actual
            

    #arriba
    if x-1 >= 0:
        if tablero[x-1][y] != 5:
            #movimiento posible, agregue a la cola
            if tablero[x-1][y] == 2 and flag==0:
                costos.put((costo+2,limite+1,x-1,y,flag)) #Se agrega una tupla que tiene el costo de la casilla y las posiciones en X & Y
                agregarElemento(arbol,(x-1,y,limite+1,flag),(x,y,limite,padre)) #Se agrega un hijo a este arbol, que tendrá como padre la pos actual
            else:
                costos.put((costo+1,limite+1,x-1,y,flag)) #Se agrega una tupla que tiene el costo de la casilla y las posiciones en X & Y
                agregarElemento(arbol,(x-1,y,limite+1,flag),(x,y,limite,padre)) #Se agrega un hijo a este arbol, que tendrá como padre la pos actual

    #Se almacena la tupla con el mejor costo 
    mejor = costos.get()
    #Se hace una recursión ingresandole los valores en X & Y del mejor costo, y el valor de ese costo
    iaCosto(mononoke,mejor[2],mejor[3],mejor[0],mejor[4],mejor[1],mejor[4],arbol)

#Profundidad iterativa
def iaIterativa(mononoke,x,y,con,flag,iterador,limite,padre,arbol):

    global contadorglobal,nodosglobal,limiteglobal,xglobal,yglobal
    if tablero[x][y] == 4: #Comprueba si la posicion actual es meta
        #Se agrega la posición de meta al array de recorrido
        flag=1
        recorrido.append((x,y,limiteglobal))
        #Llama la funcion ancestros 
        ancestros(arbol,(x,y,limiteglobal))
        mover(mononoke)
        tk.messagebox.showinfo(message="ENCONTRÓ LA META. El limite fue = "+ str(limiteglobal), title="FIN")
        return sys.exit()

    if limite > iterador or limite!=0:

        con+=1
        #derecha
        if y+1 <= 4 and flag==0:
            if tablero[x][y+1]!=5:
                contadorglobal+=1
                agregarElemento(arbol,(x,y+1,padre+1),(x,y,padre))
                if iterador < limite:
                    iaIterativa(mononoke,x,y+1,0,flag,iterador,limite-1,padre+1,arbol)
            elif con==1:
                nodosglobal-=4**(limite-1)
        elif con==1:
            nodosglobal-=4**(limite-1)
        
        con+=1
        #abajo
        if x+1 <= 3 and flag==0:
            if tablero[x+1][y]!=5:
                contadorglobal+=1
                agregarElemento(arbol,(x+1,y,padre+1),(x,y,padre))
                if iterador < limite:
                    iaIterativa(mononoke,x+1,y,0,flag,iterador,limite-1,padre+1,arbol)
            elif con==2:
                nodosglobal-=4**(limite-1)
        elif con==2:
            nodosglobal-=4**(limite-1)

        con+=1
        #izquierda
        if y-1 >= 0 and flag==0:
            if tablero[x][y-1]!=5:
                contadorglobal+=1
                agregarElemento(arbol,(x,y-1,padre+1),(x,y,padre))
                if iterador < limite:
                    iaIterativa(mononoke,x,y-1,0,flag,iterador,limite-1,padre+1,arbol)
            elif con==3:
                nodosglobal-=4**(limite-1)
        elif con==3:
            nodosglobal-= (4**(limite-1))
        
        con+=1
        #arriba
        if x-1 >= 0 and flag==0:
            if tablero[x-1][y]!=5:
                contadorglobal+=1
                agregarElemento(arbol,(x-1,y,padre+1),(x,y,padre))
                if iterador < limite:
                    iaIterativa(mononoke,x-1,y,0,flag,iterador,limite-1,padre+1,arbol)
            elif con==4:
                nodosglobal-=4**(limite-1)
        elif con==4:
            nodosglobal-=4**(limite-1)

    if flag==0 and contadorglobal==nodosglobal-1:
        limiteglobal += 1
        nodosglobal += 4 ** (limiteglobal)
        contadorglobal=0
        arbol = Arbol((xglobal,yglobal,0))
        iaIterativa(mononoke,xglobal,yglobal,0,flag,0,limiteglobal,0,arbol)
    else:
        return None

#Dibujar mononoke
def dibujarMononoke(opc):
    global xglobal,yglobal
    contador = 0
    for i in range (len(tablero)):
        for j in range (len(tablero[i])): #Se recorre la configuración del tablero para validar cuando encuentra una mononoke
            if tablero[i][j] == 1:
                xglobal =i
                yglobal =j 
                mononoke = turtle.Turtle()
                image = "mononoke2.gif"
                screen.addshape(image)
                mononoke.shape(image)
                mononoke.ht()
                mononoke.penup()
                mononoke.setposition(posiciones[i][j]) 
                mononoke.st()
                mononoke.speed(1)
                if opc == 1: #Ejecuta el algoritmo por costos 
                    tree = Arbol((xglobal,yglobal,0,0))
                    iaCosto(mononoke,xglobal,yglobal,0,0,0,0,tree)
                if opc == 2:
                    tree = Arbol((xglobal,yglobal,0))
                    iaIterativa(mononoke,xglobal,yglobal,0,0,0,0,tree.elemento,tree)

def dibujarKodama():

    for i in range (len(tablero)):
        for j in range(len(tablero[i])):#Se recorre la configuración del tablero para validar cuando encuentra un kodama
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
        for j in range (len(tablero[i])):#Se recorre la configuración del tablero para validar cuando encuentra un Yakult
            if tablero[i][j] == 3:
                image = "yakult2.gif"
                screen.addshape(image)
                yakult.shape(image)
                yakult.ht()
                yakult.penup()
                yakult.setposition(posiciones[i][j])
                yakult.st() 

def dibujarEspiritu():

    flag = 0
    for i in range (len(tablero)):
        for j in range (len(tablero[i])): #Se recorre la configuración del tablero para validar cuando encuentra un espíritu
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
        for j in range (len(tablero[i])): #Se recorre la configuración del tablero para validar cuando encuentra un árbol (obstáculo)
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

ventana = tk.Tk() #Se crea una ventana para seleccionar el tipo de IA que usará

def costo(): #Funcion para ejecutar el algoritmo de costo
    ventana.destroy()
    dibujarArbol()
    dibujarKodama()
    dibujarYakult()
    dibujarEspiritu()
    dibujarMononoke(1)

def iterativa(): #Funcion para ejecutar el algoritmo de profundidad iterativa
    ventana.destroy()
    dibujarArbol()
    dibujarKodama()
    dibujarYakult()
    dibujarEspiritu()
    dibujarMononoke(2)

def configurarJuego():
    ventana.title("Laberinto de Mononoke") #Se configura la ventana de selección de algoritmo
    ventana.geometry('300x100')
    l1 = tk.Label(ventana,text="Escoja el método")
    l1.place(x=105,y=20)
    boton1 = tk.Button(ventana,text="costo",command=costo)
    boton1.place(x=20,y=50,width=120)
    boton2 = tk.Button(ventana,text="Profundidad iterativa",command=iterativa)
    boton2.place(x=160,y=50,width=120)
    ventana.mainloop()
#hice otro cambio
configurarJuego() #Se llama la función que me configura el laberinto