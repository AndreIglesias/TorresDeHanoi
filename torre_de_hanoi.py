# ============================================================================================
# PROGRAMA   : TorreHanoi2.0.py
# AUTOR      : QED
#
# DESCRIPCION: Mi sexto programa. Aprendiendo a programar.
#              Con 3 columnas (a,b y c) con una torre de discos en a, todos los discos
#
# Reglas     : 1- solo se puede mover un disco a la vez
#              2- No se puede poner un disco mas grande sobre uno mas pequeño
#
# PROPOSITO  : Pasar los discos de la primer columna (a) a la ultima (c), en el mismo orden. 
#              rectangulo con el area mayor dentro de escaleras enumeradas.
#
# FECHA      : 17/04/2017
# ============================================================================================

# --------------------------------------------------------------------------------------------
# EXPLANATION
# --------------------------------------------------------------------------------------------


# Para resolver una torre de Hanoi, se necesita saber si hay una cantidad de
# discos par o impar, para poder mover las piezas de la torre en direcciones especificas.
# La ultima pieza siempre tiene que moverse hacia la izquierda una vez (-1 = c mod 3) o
# hacia la derecha dos veces (2 = c mod 3) para llegar al destino esperado, el cual debera
# disponible para la colocacion de la pieza mayor. A esa cantidad de discos se le denominara
# como el "grado" de una torre (el grado principal sera el grado de toda la torre).
#
# A partir de aqui, definimos que si hay un grado principal par, todos los numeros pares
# tendran la misma caracteristica que la ultima pieza (se moveran una posicion a la izquierda) y los
# impares hacia la otra dirrecion.
# En cambio, si el grado es impar, todas las piezas imares se moveran a la izquierda y los pares 
# a la derecha.
# Esta simetria en el movimiento entre los discos se da, debido a que cada uno de los discos
# es el ultimo disco en una torre parcial o interna dentro de la torre principal, por lo que 
# sigue el mismo patron.
#
# Estos discos siempre tendran un movimiento asignado, pero como la prioridad son las
# reglas iniciales del problema, si no cumplen alguna de estas, entonces se prosigue a evaluar
# el movimiento de la siguiente pieza, ignorando el de la pieza que no cumplio alguna regla inicial.
#
# Esta asignacion de movimientos genera un patron palindromo, al verse incluida la recursion,
# despues de haber movido a su lugar la primer pieza, la segunda se comporta como base de una
# torre de grado 2, la tercera pieza como base de una torre de grado 3, etc.
# Los movimientos en una torre de grado 1 se basan en mover la base, que es la unica pieza,
# hacia la izquierda una vez. El movimiento hacia cualquier sentido de la pieza "n" se denotara
# como "n", y los movimientos con varias piezas seran concatenados de derecha a izquierda.
# Asi los movimientos de la torre de grado 2 sera "1 2 1" tratando a la segunda pieza como base.
# Los de grado 3 seran "121 3 121", grado 4 "1213121 4 1213121", y asi sucesivamente.
# Siempre los movimientos de una torre de orden "n" seran los de la torre de grado anterior "n-1"  
# seguido por la base "n" y los movimientos de "n-1".
#
# La cantidad de movimientos de la pieza "m" en una torre de grado "n" sera siempre igual a 2**(n-m)


# _______________________________________________________________________________________________________
# DECLARATIONS
# _______________________________________________________________________________________________________


# --------------------------------------------------------------------------------------------------------
# VALIDATION FUNCTIONS
# --------------------------------------------------------------------------------------------------------

# Asegura que el valor a leer sea del tipo que determine la llamada a esta función
def DesinfectanteDeTipo(prompt, tipo=None, minimo = None):

    while True:
        a = input(prompt)
        if a == '': return 'break'
        if tipo is not None:
            try:
                a = tipo(a)
            except ValueError:
                print("El valor debe ser de tipo {0}. ".format(tipo.__name__))
                continue
        if minimo is not None and a < minimo:
            print("El valor debe ser mayor o igual que {0}.".format(minimo))
        else:
            return a


# Asegura un 'y' o un 'n' en la respuesta - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def whl(prompt, value = None):
    a = input(prompt)
    if (a == '') and (value is not None): return value
    elif (a == ''): return ''
    while a.lower() not in {'n', 'y'}:
        a = input(chr(27)+"[3;91m"+"Digite un valor correcto. (Y/N) "+chr(27)+"[0m")
    return a


# ------------------------------------------------------------------------------------------------------------
# VISUAL PRESENTATION
# ------------------------------------------------------------------------------------------------------------

# Carriage return <CR>, solo por presentacion)
def CR():
    print("\n")


# ____________________________________________________________________________________________________________
# GRAPHICAL INTERFACE
# ____________________________________________________________________________________________________________

import time

try:
  from tkinter import *  # python 3
except ImportError:
  from Tkinter import *  # python 2

class resize(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width = self.width, height = self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)

class graficos():

    # The class "constructor" - It's actually an initializer  - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, master, columnitas):
        self.master = master
        self.columnitas = columnitas
        self.tk = tk = Tk()
        tk.title("Torre de Hanoi")
        self.frame = f = Frame(tk, bg = "black")
        f.pack(fill = BOTH, expand = YES)
        self.canvas = c = resize(f, width=850, height=400, bg="black", highlightthickness=0)
        c.pack(fill = BOTH, expand = YES)
        width, height = tk.getint(c['width']), tk.getint(c['height'])

        # this data is used to keep track of an 
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        c.tag_bind("token", "<ButtonPress-1>", self.on_token_press)
        c.tag_bind("token", "<ButtonRelease-1>", self.on_token_release)
        c.tag_bind("token", "<B1-Motion>", self.on_token_motion)


        #ctrlFrame = Frame(tk) # contains Buttons to control the game 
        #self.resetBtn = Button(ctrlFrame, width = 11, text = "reset", state = DISABLED, padx = 15, command = self.reset)
        #self.stepBtn  = Button(ctrlFrame, width = 11, text = "step", state = NORMAL,  padx = 15, command = self.step)
        #self.startBtn = Button(ctrlFrame, width = 11, text = "start", state = NORMAL,  padx = 15, command = self.start)
        #for widget in self.resetBtn, self.stepBtn, self.startBtn:
        #    widget.pack(side = LEFT)
        #ctrlFrame.pack(side = TOP)
        #        self.state = "START"

        
        # -------------------------------------------------------------------------------------------------
        # FIGURAS
        # -------------------------------------------------------------------------------------------------

        # ----------------
        # COLUMAS
        #-----------------

        # Dimensiones - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        c_width = 14                                                    # Anchura de columna
        c_height = height // 2                                          # Altura  de columna
        c_distancia = width // 3                                        # Distancia entre columna

        # Coordenadas de columna (rectangulo) - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        x1, y1 = ((c_distancia - c_width) // 2), (height // 3)
        x2, y2 = (x1 + c_width), (y1 + c_height)

        # Dimensionando las columnas - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.columnas = []                                              # Lista de columnas

        for i in range(3):                                              # Genera las 3 columnas en blanco

            col = c.create_rectangle(x1, y1, x2, y2, fill = 'white')
            self.columnas.append(col)
            x1, x2 = (x1 + c_distancia), (x2 + c_distancia)

        self.tk.update()

        # ----------------
        # DISCOS
        #-----------------

        # Dimensiones  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        D_max_width = c_width * 7                                      # Anchura maxima y minima de disco
        D_min_width = c_width *1.5
        D_height    = c_height // 16                                    # Altura  de disco
        D_distancia = (D_max_width - D_min_width) // (2 * max(1, master - 1))  # Distancia entre discos


        # Coordenadas de disco (rectangulo) - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        x1, y1 = ((c_distancia - D_max_width) // 2), (y2 - D_height // 3)
        x2, y2 = (x1 + D_max_width), (y1 + D_height)

        # Generador de discos en las columnas - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #self.columnitas = [ [], [], [] ]
        self.discos = {}
        colores = ['slateBlue', 'cyan2', 'forest green', 'chartreuse', 'yellow', 'orange red', 'red', ]
        r = 0                                                           # contador para la posicion de colores

        for i in range(master, 0, -1):                                       # Genera los discos desde el disco n (el mas pequeño) hasta 0
            disc = c.create_rectangle(x1, y1, x2, y2, fill = colores[r % len(colores)], tags = 'token')
            self.discos[i] = disc                                       # Agrega las figuras de los discos a 'discos'
            #self.columnitas[0].append(i) # A REEMPLAZAR.REVERSE()       # Añade los discos a la primer columna (elemento 0 en columnitas)
                                                                        # [ [n, n-1, n-2, ..., 1], [], [] ]

            x1, x2 = (x1 + D_distancia), (x2 - D_distancia)             # Modifica las dimensiones para los siguientes discos
            y1, y2 = (y1 - D_height - 2), (y2 - D_height - 2)
            r     += 1                                                  # contador
            self.tk.update()
            self.tk.after(25)


    def on_token_press(self, event):
        c = self.canvas
        '''Begining drag of an object'''
        # record the item and its location
        self._drag_data["item"] = c.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_token_release(self, event):
        ax1, ay1, ax2, ay2 = c.bbox(self.columnas[0]) 
        bx1, by1, bx2, by2 = c.bbox(self.columnas[1])
        cx1, cy1, cx2, cy2 = c.bbox(self.columnas[2]) 
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_token_motion(self, event):
        c = self.canvas
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        c.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y


    def ViajeDiscos(self, viajero, a, b, game = None):
        if self.columnitas[a][0] != viajero: raise RuntimeError # Assertion
        if self.columnitas[a] != []: del self.columnitas[a][0]          
        disc = self.discos[viajero]
        c = self.canvas

        # Levantar encima de la columna 'a'
        ax1, ay1, ax2, ay2 = c.bbox(self.columnas[a])                   # Coordenadas de la columna 'a' ...
        while 1:
            x1, y1, x2, y2 = c.bbox(disc)
            if y2 < ay1: break
            c.move(disc, 0, -1)
            self.tk.update()
            time.sleep(0.002)

        # Mover hasta la columna 'b'
        bx1, by1, bx2, by2 = c.bbox(self.columnas[b])                   # Coordenadas de la columna 'b' ...
        newcenter = (bx1+bx2)//2
        while 1:
            x1, y1, x2, y2 = c.bbox(disc)
            center = (x1 + x2) // 2
            if center == newcenter: break
            if game is None:
                if center > newcenter: c.move(disc, -1, 0)
                else: c.move(disc, 1, 0)
            self.tk.update()
            time.sleep(0.0045)  
            c.addtag_all("all")

        # Bajar la pieza hasta la parte de arriba de la primera pieza de la columna 'b' - - - - - - - - - - 
        D_height = y2-y1
        newbottom = by2 - D_height*len(self.columnitas[b]) - 2 
        while 1:
            x1, y1, x2, y2 = c.bbox(disc)
            if y2 >= newbottom: break
            if (self._drag_data["item"] != None) or (game is None):  
                c.move(disc, 0, 1)
                self.tk.update()
                time.sleep(0.002)
            else: break
        if b == 0:
            c.move(disc, 0, 9)
            self.tk.update()

        # Regresar al estado anterior 'columnitas' - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if self.columnitas[b] != []:
            self.columnitas[b].insert(0, viajero)
        else:
            self.columnitas[b].append(viajero)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # GUI for animated towers-of-Hanoi-game with upto 10 discs:
'''
    def displayMove(self, move):
        """method to be passed to the Hanoi-engine as a callback
        to report move-count"""
        self.moveCntLbl.configure(text = "move:\n%d" % move)
    
    def adjust_nr_of_discs(self, e):
        """callback function for nr-of-discs-scale-widget"""
        self.hEngine.nrOfDiscs = self.discs.get()
        self.reset()

    def adjust_speed(self, e):
        """callback function for speeds-scale-widget"""
        self.hEngine.speed = self.tempo.get()

    def setState(self, STATE):
        """most simple representation of a finite state machine"""
        self.state = STATE
        try:
            if STATE == "START":

                self.resetBtn.configure(state=DISABLED) # reset(self):   self.algo.reset()     self.setState("START")  restores START state for a new game
                self.startBtn.configure(text="start", state=NORMAL)
                self.stepBtn.configure(state=NORMAL)
            elif STATE == "RUNNING":
                self.resetBtn.configure(state=DISABLED)
                self.startBtn.configure(text="pause", state=NORMAL)
                self.stepBtn.configure(state=DISABLED)
            elif STATE == "PAUSE":
                self.resetBtn.configure(state=NORMAL)
                self.startBtn.configure(text="resume", state=NORMAL)
                self.stepBtn.configure(state=NORMAL)
            elif STATE == "DONE":
                self.resetBtn.configure(state=NORMAL)
                self.startBtn.configure(text="start", state=DISABLED)
                self.stepBtn.configure(state=DISABLED)
            elif STATE == "TIMEOUT":
                self.resetBtn.configure(state=DISABLED)
                self.startBtn.configure(state=DISABLED)
                self.stepBtn.configure(state=DISABLED)

        except TclError: pass

    def start(self):
        # callback function for start button, which also serves as pause button. Makes hEngine running until done or interrupted
        if self.state in ["START", "PAUSE"]:
            self.setState("RUNNING")            
            if self.hEngine.run():
                self.setState("DONE")
            else:
                self.setState("PAUSE")
        elif self.state == "RUNNING":
            self.setState("TIMEOUT")
            self.hEngine.stop()

    def step(self):
        # callback function for step button. makes hEngine perform a single step
        self.setState("TIMEOUT")
        if self.hEngine.step():
            self.setState("DONE")
        else:
            self.setState("PAUSE")






global pts

ndiv = slider.get()
          
'''

# _________________________________________________________________________________________________________
# MAIN
# _________________________________________________________________________________________________________


def main():

    # -----------------------------------------------------------------------------
    # MAIN FUNCTIONS
    # -----------------------------------------------------------------------------

    def SiGui(i,a,b):
        if ConGui is 'y' or ConGui is 'Y':
            if (Autoresovlver.lower() in {'y', ''}):
                clase.ViajeDiscos(i, a, b)
            else:
                clase.ViajeDiscos(i, a, b, game = 'y')

    # Movimientos de los discos antes mencionados
    def Movimientos(a,b,c):
        if cantidad%2 == 0:
            if Elemento%2 == 0:
                SiGui(columnitas[c][0], c, a)
                #columnitas[a].insert(0, columnitas[c].pop(0))
            else:
                SiGui(columnitas[c][0], c, b)
                #columnitas[b].insert(0, columnitas[c].pop(0))
        else:
            if Elemento%2 == 0:
                SiGui(columnitas[c][0], c, b)
                #columnitas[b].insert(0, columnitas[c].pop(0))
            else:
                SiGui(columnitas[c][0], c, a)
                #columnitas[a].insert(0, columnitas[c].pop(0))

    # Imprime la serie de pasos a seguir
    def imprimir():
        a.reverse()
        b.reverse()
        c.reverse()
        print("columna a :", a)
        print("columna b :", b)
        print("columna c :", c)
        a.reverse()
        b.reverse()
        c.reverse()
        print("---------------------------------------------------------------------"*2)

    # condiciones que deben cumplir los casos en particular cuando la pieza a evaluar se encontraba en la lista EncontradoEn
    def condiciones(EncontradoEn,b,c):
        return  EncontradoEn != [] and EncontradoEn[0] == Elemento and (b == [] or b[0] > EncontradoEn[0] or c == [] or c[0] > EncontradoEn[0])


    '''def fcantidad(value = None):
        if value is None: confirmar = 'n' # centinela
        else: confirmar = value
        print(value)
        cantidad = DesinfectanteDeTipo("Cantidad de discos a pasar: ", tipo = int, minimo = 0)
        if confirmar.lower() not in {'y', ''}:
            if cantidad == 'break': 
                confirmar = whl('¿Seguro de que quere salir? (Y/N) ')
                if confirmar.lower() not in {'y',''}: fcantidad(value = 'y')                
        if (value is None) and (confirmar.lower() in {'y', ''}): return confirmar
        else: return cantidad'''


    # _________________________________________________________________________________________________________
    # MAIN BODY
    # _________________________________________________________________________________________________________

    CR()
    CONDICION = whl("¿Encontrar pasos para resolver una Torre de Hanoi? (Y/N) ", 'y')   
    CR()

    Proseguir, confirmar, ConGui = 'y', 'n', 0

    while (CONDICION is "Y" or CONDICION is "y"):

        cantidad = DesinfectanteDeTipo("Cantidad de discos a pasar: ", tipo = int, minimo = 0)
        if cantidad == 'break': 
            confirmar = whl('¿Seguro de que quere salir? (Y/N) ')
            if confirmar.lower() not in {'y', ''}: cantidad = DesinfectanteDeTipo (
                "Cantidad de discos a pasar: ", tipo = int, minimo = 0
                )
            if cantidad == 'break': break

        if confirmar.lower() in {'y', ''}: break                                                                                            

        a, b, c, D = [], [], [], []
        pasos=0 
        for l in range(cantidad):
            a.append(l+1)
            D.append(l+1)
            pasos = 2*pasos+1 
        # Cantidad de pasos por hacer, a = [1,2,3,4,...,n] donde cada numero respresenta el nivel desde arriba hacia abajo

        CR()
        Proseguir = whl("Seran {} pasos. ¿Desea continuar? (Y/N) ".format(pasos), 'y')
        if Proseguir.lower() not in {'y'}:
            confirmar = whl('¿Seguro de que quere salir? (Y/N) ', 'y')
        if confirmar.lower() in {'y'}: break

        ConGui = whl('¿Visualizar con Interfaz Grafica? (Y/N) ', 'y')
        if ConGui.lower() in {'y'}:
            columnitas = [a,b,c]
            master = cantidad
            Autoresovlver = whl('¿Resolver de manera automatica? (Y/N) ')

            clase = graficos(master, columnitas)



        imprimir()
        i = 0                                                                                                                                                  
        while c != D:
            columnitas = [a,b,c]

            Elemento = D[i%cantidad]
            i += 1
            if  condiciones(a,b,c):         # condiciones    a, b, c
                
                Movimientos(2,1,0)          # Movimientos    c, b, a     # columnitas[2], columnitas[1], columnitas[0]
                imprimir()

            elif condiciones(b,a,c):        # condiciones    a, b, c
               
                Movimientos(0,2,1)          # Movimientos    a, c, b    # columnitas[0], columnitas[2], columnitas[1]
                imprimir()

            elif condiciones(c,b,a):        # condiciones    c, b, a
                
                Movimientos(1,0,2)          # Movimientos    b, a, c    # columnitas[1], columnitas[0], columnitas[2]
                imprimir()

        print("Cantidad minima de pasos necesarios: ", pasos)

        CR()
        CONDICION = whl("Resolver más Torres? (Y/N) ", 'y')
        CR()
# -----------------------------------------------------------------------------------------------

    CR()
    print("Fin del programa.")
    CR()


# Cuando se esta ejecutando como programa principal y no como una llamada a un modulo
if __name__ == '__main__':
    main()
