from MetodoSimplex import *
# Clase que representa la tabla utilizada para la realización del método de la GranM.
# Hereda sus atributos y métodos de la clase MetodoSimplex.
class MetodoGranM(MetodoSimplex):

    # Constructor de la clase.
    def __init__(self, matriz = [], actuales = [], artificiales=[], contador=0, estado="Normal", numPivote=0,
                 filaPivote=0, coluPivote=0):
        # Llama al método constructor de la clase MetodoSimplex
        MetodoSimplex.__init__(self, matriz, actuales, artificiales, contador, estado, numPivote, filaPivote, coluPivote)

    # Función para cargar la tabla a partir de la entrada.
    def cargar(self, entrada):
        GranM = 1000            # Número utilizado como "GranM".
        matriz = []             # Matriz donde se almacenan los datos.
        actuales = []           # Lista de variables actuales de la tabla.
        artificiales = []       # Lista de variables artificiales de la tabla.
        restricciones = entrada.cantidadRestricciones           # Cantidad de restricciones
        variablesDecision = entrada.cantidadVariablesDecision   # Cantidad de variables de decisión.
        listaVariablesDecision = entrada.tabla[0][:entrada.cantidadVariablesDecision]   # Lista de variables de decisión
        matriz.append(listaVariablesDecision)       # Se inserta el primer renglón.
        contador = 0            # Contador para saber cuántas variables han sido insertadas.
        # Por la cantidad de restricciones se va añadiendo una fila.
        for i in range(restricciones):
            restriccionActual = entrada.tabla[i + 1]    # Se obtiene la restricción en la posición i.
            matriz.append(restriccionActual[:-1])       # Se añaden los coeficientes de las variables de decision.
            matriz[-1] += [0] * contador                # Se añaden los ceros que corresponden.

            # Si la restricción es <=.
            if (entrada.restriccion[i] == "<="):
                matriz[0].append(0)     # Se añade un cero en la primera fila.
                matriz[-1].append(1)    # Se añade la variable de holgura en la fila i.
                actuales.append(variablesDecision + contador)   # Se añade la nueva variable como actual.

            # Si la restricción es =.
            elif (entrada.restriccion[i] == "="):
                matriz[0].append(GranM) # Se añade el valor de GranM en la primera fila.
                matriz[-1].append(1)    # Se añade un 1 en la fila i.
                actuales.append(variablesDecision + contador)       # Se añade la nueva variable como actual.
                artificiales.append(variablesDecision + contador)   # Se añade la nueva variable como artificial.

            # Si la restricción es >=.
            else:
                matriz[0].append(0)     # Se añade un cero en la primera fila.
                matriz[-1].append(-1)   # Se añade la variable de exceso en la fila i.
                contador += 1           # Se aumenta el contador en 1.

                matriz[0].append(GranM) # Se añade el valor de GranM en la primera fila.
                matriz[-1].append(1)    # Se añade un 1 en la fila i.
                actuales.append(variablesDecision + contador)       # Se añade la nueva variable como actual.
                artificiales.append(variablesDecision + contador)   # Se añade la nueva variable como artificial.

            matriz[-1].append((restriccionActual[-1]))              # Se añade el lado derecho de la fila.
            contador += 1               # Se aumente al contador.

        matriz[0].append(0)             # Finalmente se añade el lado derecho de la primera fila.

        largo = len(matriz[0])          # Se obtiene el largo de la primera fila.
        for i in range(restricciones):  # Por cada fila de la matriz menos la primera.
            falta = largo - len(matriz[i + 1])  # Se calculan los ceros que le falta.
            matriz[i + 1][:-1] += [0] * falta   # Se añaden los ceros que le falta.

            if (actuales[i] in artificiales):   # Si la fila actual posee una artificial.
                operaEntreFilas(matriz[i + 1], matriz[0], -GranM)   # Se realiza la operación para dejar en 0 su
                                                                    # posición correspondiente en el primer renglón.
        # Se asignan los valores resultantes.
        self.matriz = matriz
        self.actuales = actuales
        self.artificiales = artificiales

    # Función para resolver el método de la Gran M.
    def resolver(self,optimizacion):

        respuesta = simplex(self)       # Se realiza el método Simplex con la tabla actual.

        # Si la optimización era una minimización se multiplica por -1 toda la primera fila.
        if (optimizacion == "min"):
            respuesta[-1].matriz[0] = [elemento * -1 for elemento in respuesta[-1].matriz[0]]

        return respuesta                # Se retorna la respuesta.