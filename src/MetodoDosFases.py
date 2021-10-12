from MetodoSimplex import *
import sys


# Clase utilizada para representar los problemas de tipo dos fases, hereda de la clase MetodoSimplex unicamente posee
# una lista con las variables de exceso en comparación a dicha clase.
class MetodoDosFases(MetodoSimplex):

    # Constructor de la clase, recibe como parametros una matriz que representa la tabla del problema,
    # una lista de las variables basicas actuales, lista de variables artificiales, lista de las variables
    # de acceso, un contador del número de iteración, el estado: Normal, No acotada, Soluciones muntiples, etc,
    # número pivote y la columna pivote.
    def __init__(self, matriz=[], actuales=[], artificiales=[], exceso=[], contador=0, estado="Normal", numPivote=0,
                 filaPivote=0,
                 coluPivote=0):
        MetodoSimplex.__init__(self, matriz, actuales, artificiales, contador, estado, numPivote, filaPivote,
                               coluPivote)
        self.exceso = exceso

    # Este metodo es utilizado para cargar los datos extraidos del archivo de origen, que contiene el problema a resolver
    # y carga los datos obtenidos en el objeto MetodoDosFases y prepararse para ejecutar el algoritmo de Dos Fases
    def cargar(self, entrada):
        # Calculo la cantidad de que se tienen que agredar, cuando la restriccion es de "=" o "<=" unicamente se tendria
        # que agregar una variable por restriccion, mientras que con ">=" serian 2
        cantidadVariables = entrada.restriccion.count("<=") + entrada.restriccion.count("=") + (
                2 * entrada.restriccion.count(">="))
        # En la columna 0, ingresamos las variables del archivo y se le añaden los ceros de las variables de holgura,
        # exceso o artificiales necesarios para resolver el problema.
        self.matriz.append(entrada.tabla[0] + [0] * cantidadVariables)
        posicion = 0  # Se utiliza para llevar un conteo de la posicion en columna de los  valores que se ingresan.

        # Se procede a procesar las restricciones
        for i in range(entrada.cantidadRestricciones):
            temp = [
                       0] * cantidadVariables  # Este arreglo de ceros, es donde se colocan los valores de las nuevas variables
            if entrada.restriccion[i] == "<=":  # Caso de restricción "<="
                self.actuales.append(posicion + entrada.cantidadVariablesDecision)   # Se agrega la variable a las vb,
                # que son representadas por la lista actuales
                temp[posicion] = 1 # Ingresamos un 1 el la columna de la nueva variable de holgura
                posicion += 1 # Aumenta el contador de columnas
                temp = entrada.tabla[i + 1][:-1] + temp + entrada.tabla[i + 1][-1:] # Unimos la los datos del archivo de
                # entrada con los valores de las nuevas variables
                self.matriz.append(temp)    # Se añade a la matriz la nueva fila
            elif entrada.restriccion[i] == '=': # Caso de restrición "="
                self.actuales.append(posicion + entrada.cantidadVariablesDecision)  # Se agrega la variable a las vb
                self.artificiales.append(posicion + entrada.cantidadVariablesDecision) # Se agrega la variable a las artificiales
                temp[posicion] = 1  # Colocamos un uno en la posicion de la variable
                posicion += 1 # Aumenta el contador de columnas
                temp = entrada.tabla[i + 1][:-1] + temp + entrada.tabla[i + 1][-1:] # Se une la entrada original con las nuevas variables
                self.matriz.append(temp)    # Se añade a la matriz la nueva fila
            elif entrada.restriccion[i] == ">=":    # Caso de restricción >="
                self.exceso.append(posicion + entrada.cantidadVariablesDecision)    # Se añade una variable de exceso
                temp[posicion] = -1 # Se coloca un -1 en la posición de la variable
                posicion += 1 # Aumenta el contador de columnas
                self.artificiales.append(posicion + entrada.cantidadVariablesDecision) # Se añade una variable artificial
                self.actuales.append(posicion + entrada.cantidadVariablesDecision) # Añadimos la variables a la lista de vb
                temp[posicion] = 1 # Se coloca un 1 en la posición de la variable
                posicion += 1 # Aumenta el contador de columnas
                temp = entrada.tabla[i + 1][:-1] + temp + entrada.tabla[i + 1][-1:]     # Se une la entrada original con las nuevas variables
                self.matriz.append(temp)    # Se añade a la matriz la nueva fila

    # Metodo utilizado para realizar la primera fase del metodo
    def primeraFase(self):
        # Se crea una lista para representar la nueva función objetivo
        nuevaFunObj = [0] * len(self.matriz[0])
        # En la nueva función objetivo colocamos un -1 en la posición de las variables artificiales
        for x in self.artificiales: # Se recorre la lista de las artificiales
            nuevaFunObj[x] = -1 # Se coloca un -1 en las columnas de funciones artificiales
        # Ahora debemos convertir los valores de las vb en z a ceros para continuar, por lo que se itera entre filas
        for i in range(len(nuevaFunObj)):   #Iteramos
            for j in range(1, len(self.matriz)): # Se recorre las filas
                if self.actuales[j - 1] in self.artificiales: # Si la columna es de una variable artificial
                    nuevaFunObj[i] += self.matriz[j][i] # Se suma el valor a la función objetivo
            nuevaFunObj[i] *= -1    # Se multiplica por -1 a los valores de la función objetivo para "despejarla"
        self.matriz = [nuevaFunObj] + [x for x in self.matriz[1:]]  # Remplazamos la función objetivo de la columna

    # Metodo utilizado para preparar la segunda fase del problema de dos fases, recibe la última tabla de la primera
    # face y la función objetivo original
    def segundaFase(self, problema, funcObj):
        matriz = problema.matriz    # Se utiliza para mejor comprensión o lectura
        actuales = problema.actuales    # Se utiliza para mejor comprensión o lectura
        artificiales = problema.artificiales    # Se utiliza para mejor comprensión o lectura
        if round(matriz[0][-1], 6) != 0: # Comprobamos si el valor de z en la última tabla es distinto a 0 para seguir
            sys.exit("No se puede continuar a la segunda Fase, el problema no tiene solucion factible") # Se detiene si es 0
        temp = [0] * len(matriz[0]) # Procedemos a colocar la función original
        for i in range(len(funcObj)): # Iteramos la función objetivo original
            temp[i] = -funcObj[i] # Colocamos en la nueva
        matriz[0] = temp # Cambiamos la función objetivo del problema

        # Se verifica si las vb son cero en la función objetivo
        for i in actuales: # Se itera la lista de actuales (vb)
            if (matriz[0][i] != 0): # Si no es cero
                x = actuales.index(i)
                operaEntreFilas(matriz[x + 1], matriz[0], -matriz[0][i]) # Se procede a realizar operaciones entre filas para convertirlos en cero

        # Ahora se eliminan las variables artificiales de la tabla
        artificiales.reverse() # Invertimos la lista de variables artificiales para eliminar las columnas de derecha a izquierda
        for i in range(len(artificiales)):  # Se itera la lista de artificiales
            for j in range(len(matriz)):    # Se recorre las filas de la tabla
                matriz[j].pop(artificiales[i])  # Se extra las columnas artificiales
        matriz[0] = [elemento * -1 for elemento in matriz[0]] # Se multiplica con -1 para despejar la función objetivo
        self.matriz = matriz    # Se actualiza el valor de la matriz del objeto
        self.actuales = actuales # Se actualiza el valor de la lista de actuales del objeto
