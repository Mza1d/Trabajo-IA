#Univ.: Anarata Diaz Mario

#AGENTES QUE PLANIFICAN - AGENTE BASADO EN OBJETIVOS

#IMPORTAMOS LIBRERIAS
import random as rd # para Aleatorio
import matplotlib.pyplot as plt #Para graficar

def main():
    agente = input("\tSELECCIONE\nAgente reactivo simple '0' \nAgente basado en objetivos '1'\n")
    matriz = definirAmbiente() #crea ambiente
    # muestra el entorno en la consola
    for i in matriz:
        print(i)
    posicion = [1,1] #posicion inicial
    puntos = 0 #iniciar puntos variables
    accion = 0 #iniciar acción variable
    if( agente == '1'): #Agente basado en objetivo
        estado = estadoActual(matriz,posicion) #estado en la posicion actual
        percepcion = [posicion,estado] #percepcion que contiene posicion + estado
        mostrar(matriz,percepcion[0]) #muestra el entorno
        while(accion != 6): #hasta que se alcance la meta
            accion = agenteObjetivo(matriz,percepcion,comprobarObjetivo(matriz)) #guarda la acción que debe realizar el Aspirador o limpiador
            if(accion != 6): # si no fuera por que la aspiradora se detuviera
                puntos +=1 #contar puntos
                percepcion = ejecutarAccion(matriz,percepcion,accion) #ejecución
                mostrar(matriz,percepcion[0]) #mostrar mapa
        print('Puntaje total: '+str(puntos)) #imprimir los puntos

        #Agente reactivo simple
    elif(agente == '0'):
        posicion= [rd.choice([1,2,3,4]),rd.choice([1,2,3,4])] #posicion inicial aleatoria de la aspiradora 
        estado = estadoActual(matriz,posicion) #estado
        percepcion = [posicion,estado] #percepcion que contiene posicion + estado
        mostrar(matriz,percepcion[0]) #mostrar
        mapa = funcionMapa() # función de mapa
        while True: # Circulo
            percepcion = ejecutarAccion(matriz,percepcion, agenteReativoSimples(matriz,mapa,percepcion))  #percepcion del robot después de ejecutar la acción      
            mostrar(matriz,percepcion[0]) #mostrar
    
    
def mostrar(I, posicion):    
    plt.imshow(I)
    plt.nipy_spectral() 
    plt.plot(posicion[0],posicion[1], marker='H', color='r', ls='')
    plt.pause(0.25)    
    #plt.clf()
    
'''
Define el entorno
1 = pared
0 = limpio
2 = sucio -> donde las posiciones de suciedad son aleatorias
'''
def definirAmbiente():
    matriz = [[1,1,1,1,1,1],
              [1,rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),1],
              [1,rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),1],
              [1,rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),1],
              [1,rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),1],
              [1,1,1,1,1,1]]
    return matriz

def funcionMapa(): # funcion Mapa
    funcionMapa = [[1,1,4],
                    [2,1,4],
                    [3,1,4],
                    [4,1,2],
                    [4,2,3],
                    [3,2,3],
                    [2,2,2],
                    [2,3,4],
                    [3,3,4],
                    [4,3,2],
                    [4,4,3],
                    [3,4,3],
                    [2,4,3],
                    [1,4,1],
                    [1,3,1],
                    [1,2,1]]
    return funcionMapa

def estadoActual(matriz,posicion): # devuelve el estado actual en la posicion dada
    return matriz[posicion[1]][posicion[0]]

def agenteObjetivo(matriz,percepcion,objObtenido):

    if(objObtenido == 0): # si se cumplió el objetivo
        return 6 # para detener
    
    posicion = percepcion[0] #posicion atual
    estado = estadoActual(matriz,posicion) #estado actual
    posicionObj = encontrarSuciedadMenorDistancia(matriz,percepcion[0]) #posicion Objetivo

    if(estado == 2): #si esta sucio
        print('Estado: '+str(estado)+' accion: aspirar')
        return 'aspirar'    
    if(posicion[1] < posicionObj[0]): #Bajar
        print('Estado: '+str(estado)+' accion: abajo')
        return 'abajo'
    elif(posicion[1] > posicionObj[0]): #Subir
        print('Estado: '+str(estado)+' accion: arriba')
        return 'arriba'
    if(posicion[0] < posicionObj[1]): #Derecha
        print('Estado: '+str(estado)+' accion: derecha')
        return 'derecha'
    elif(posicion[0]>posicionObj[1]): #Izquierda
        print('Estado: '+str(estado)+' accion: izquierda')
        return 'izquierda'
    
def comprobarObjetivo(matriz):
    for s in matriz:
        for n in s:
            if(n == 2):
                return 1
    return 0

#busca la suciedad más cercana al robot
def encontrarSuciedadMenorDistancia(matriz,posicion):
    if(estadoActual(matriz,posicion)==2): #si está sucio, vuelve a la posicion actual
        return posicion
    menorDistancia = 99999 #inicializar la variable de distancia más corta
    posicionSuciedad = posicion #inicializar la posicion de suciedad
    numLinea = 0 #contador de linea
    for linea in matriz:
        numCasa = 0 #contador de la casa
        for casa in linea:
            #si la casa esta sucia
            if(casa == 2):
                suciedad = [numLinea,numCasa] #posicion de suciedad

                distancia = calcularDistancia(posicion,suciedad) #distancia a la suciedad
                if(distancia < menorDistancia): #compara para encontrar la distancia más pequeña, si es más pequeña, guarda la posicion
                   menorDistancia = distancia 
                   posicionSuciedad = suciedad
            numCasa +=1                   
        numLinea +=1
    return posicionSuciedad

def calcularDistancia(posicionActual,posicionSuciedad): #devuelve la distancia desde la posicion actual hasta la posicion de suciedad
    cont = 0 # contador de distancia
    x = posicionActual[0] #posicion actual
    y = posicionActual[1]
    xObj = posicionSuciedad[1] #posicion objetivo
    yObj = posicionSuciedad[0]
    cont += distanciaRecta(y, yObj)
    cont += distanciaRecta(x, xObj)
    return cont

def distanciaRecta(pos, obj): # distancia entre dos puntos de fila o columna
    i = 0
    while pos != obj: 
        if pos > obj:
            pos -= 1
            i+=1
        else:
            pos +=1
            i+=1
    return i
    

#mueve el robot en función de la acción informada               
def ejecutarAccion(matriz,percepcion,accion):
    posicion = percepcion[0] # tomar la posicion del robot
    estado = percepcion[1]  # obtener el estado actual
    
    # si para verificar la acción, cambie la posicion del robot y verifique el estado
    if accion =='arriba':
        posicion = [posicion[0],posicion[1]-1]
        estado = estadoActual(matriz,posicion)
    elif accion =='abajo':
        posicion = [posicion[0],posicion[1]+1]
        estado = estadoActual(matriz,posicion)
    elif accion =='izquierda':
        posicion = [posicion[0]-1,posicion[1]]
        estado = estadoActual(matriz,posicion)
    elif accion =='derecha':
        posicion = [posicion[0]+1,posicion[1]]
        estado = estadoActual(matriz,posicion)
    elif accion =='aspirar':
        matriz[posicion[1]][posicion[0]] = 0
        estado = estadoActual(matriz,posicion)
    
    percepcion = [posicion,estado] # guardar la información en la percepcion
    return percepcion # devuelve la nueva percepcion con la nueva posicion y estado del robot

def agenteReativoSimples(matriz,mapa,percepcion): # devuelve la acción que debe realizar el robot
    posicion = percepcion[0] # robot de toma de posicion
    estado = estadoActual(matriz,posicion) # obtener estado robot
    
    if(estado == 2): #verificar estado
        return 'aspirar'
    else:
        for a in mapa: # busca la acción que debe realizar el robot
            if(a[0] == posicion[0]) and (a[1] == posicion[1]):
                if a[2] == 1:
                    print('Estado: '+str(estado)+' accion: arriba')
                    return 'arriba'
                elif a[2] == 2:
                    print('Estado: '+str(estado)+' accion: abajo')
                    return 'abajo'
                elif a[2] == 3:
                    print('Estado: '+str(estado)+' accion: izquierda')
                    return 'izquierda'
                elif a[2] == 4:
                    print('Estado: '+str(estado)+' accion: derecha')
                    return 'derecha'
main()