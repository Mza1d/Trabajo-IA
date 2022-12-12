#CONSTANTES
VACIO = 0
MURO = 1
QUESO = 2
RATA = 3

IZQUIERDA = 0
ARRIBA = 1
DERECHA = 2
ABAJO = 3
INVALIDO = -1

class Rata:
  def __init__(self, fila, columna):
    self.fila = fila
    self.columna = columna
    self.movimiento = -1 #valor inicial
    self.tuvoExito = False #valor inicial

  def verArriba(self, ambiente):
    if self.fila <= 0:
      return MURO
    if ambiente[self.fila - 1][self.columna] == 1:
      return MURO
    return VACIO
    
  def verAbajo(self, ambiente):
    if self.fila >= len(ambiente) - 1:
      return MURO
    if ambiente[self.fila + 1][self.columna] == 1:
      return MURO
    return VACIO

  def verDerecha(self, ambiente):
    if self.columna >= len(ambiente[0]) - 1:
      return MURO
    if ambiente[self.fila][self.columna + 1] == 1:
      return MURO
    return VACIO

  def verIzquierda(self, ambiente):
    if self.columna <= 0:
      return MURO
    if ambiente[self.fila][self.columna - 1] == 1:
      return MURO
    return VACIO

  #Definir movimiento que debe realizar el agente según la tabla de asociación
  def definirMovimiento(self, ambiente, decision):
    self.movimiento = decision[self.verIzquierda(ambiente), 
    self.verArriba(ambiente), self.verDerecha(ambiente), self.verAbajo(ambiente)]
    self.tuvoExito = self.olerQueso(ambiente)
    return self.movimiento
  
  #Cambiar la posición del agente en la matriz de ambiente y en lo que conoce de sí mismo
  def moverse(self, ambiente):
    ambiente[self.fila][self.columna] = VACIO
    if self.movimiento == IZQUIERDA: #a la izquierda
      self.columna = self.columna - 1
    elif self.movimiento == ARRIBA: #a arriba
      self.fila = self.fila - 1
    elif self.movimiento == DERECHA: #a la derecha
      self.columna = self.columna + 1
    elif self.movimiento == ABAJO: #a abajo
      self.fila = self.fila + 1
    ambiente[self.fila][self.columna] = RATA

  #Detectar si la casilla a la cual está a punto de moverse tiene el queso o no
  def olerQueso(self, ambiente):
    if self.movimiento == IZQUIERDA:
      verFila = self.fila
      verColumna = self.columna - 1
    elif self.movimiento == ARRIBA:
      verFila = self.fila - 1
      verColumna = self.columna
    elif self.movimiento == DERECHA:
      verFila = self.fila
      verColumna = self.columna + 1
    elif self.movimiento == ABAJO:
      verFila = self.fila + 1
      verColumna = self.columna
    #Revisar si hay queso en la casilla
    return ambiente[verFila][verColumna] == QUESO