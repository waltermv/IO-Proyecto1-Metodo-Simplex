from fractions import Fraction
# Clase que representa la tabla utilizada para la realización del método Simplex.
class MetodoSimplex:
    # Constructor de la clase.
    def __init__(self, matriz = [], actuales = [], artificiales=[], contador=0, estado="Normal", numPivote=0,
                 filaPivote=0, coluPivote=0):
        self.matriz = matriz                # La matriz en la que se colocarán los valores de las ecuaciones.
        self.actuales = actuales            # Lista que indica cuales variables se encuentran como variables básicas.
        self.artificiales = artificiales    # Lista que indica cuales variables son artificiales.
        self.contador = contador            # Contador que cuenta el número de tabla.
        self.estado = estado                # Variable que indica el estado actual de la tabla
                                            # entre "Normal", "Degenerada", "No acotada",
                                            # "Soluciones múltiples" o "Sin solución factible"
        self.numPivote = numPivote          # Variable que representa el número pivote actual.
        self.filaPivote = filaPivote        # Almacena el valor de la fila pivote.
        self.coluPivote = coluPivote        # Representa la posición de la columna pivote.

    # Método para cargar la tabla a partir de la entrada.
    def cargar(self, entrada):
        # Se cargan las variables básicas salientes.
        self.actuales = [x + entrada.cantidadRestricciones for x in range(entrada.cantidadRestricciones)]
        # Se carga el primer renglón de la matriz.
        self.matriz.append(entrada.tabla[0] + ([0] * entrada.cantidadRestricciones))
        # Se cargan los demás renglones de la matriz.
        for i in range(1, entrada.cantidadRestricciones + 1):
            temp = entrada.tabla[i][:-1] + ([0] * entrada.cantidadRestricciones) + entrada.tabla[i][-1:]
            temp[entrada.cantidadVariablesDecision + i - 1] = 1
            self.matriz.append(temp)

    # Método para crear una nueva tabla a partir de una ya existente.
    @classmethod
    def copiarTabla(cls, tablaC):
        matriz = [fila[:] for fila in tablaC.matriz]    # Se copia la matriz existente, se hace de esta
                                                        # forma porque normalmente se pasaría por referencia.
        actuales = tablaC.actuales[:]                   # Se copia la lista de variables básicas.
        artificiales = tablaC.artificiales[:]           # Se copia la lista de variables artificiales.
        contador = tablaC.contador + 1                  # Se utiliza el mismo contador pero aumentado en 1.
        estado = "Normal"                               # Se copia el estado anterior.
        numPivote = tablaC.numPivote                    # Se guarda el número pivote anterior ########
        filaPivote = tablaC.filaPivote                  # Se almacena el valor de la fila pivote.
        coluPivote = tablaC.coluPivote                  # Se almacena el valor de la columna pivote.
        return cls(matriz, actuales, artificiales,      # Se retorna la nueva tabla.
                   contador, estado, numPivote, filaPivote, coluPivote)

# Función capaz de sumar en una fila los valores de otra multiplicada por un coeficiente.
def operaEntreFilas(fila1, fila2, coeficiente):
    if (coeficiente != 0):          # Si el coeficiente es 0 no se realiza ninguna iteración.
        largo = len(fila1)
        for i in range(largo):      # Se recorre el largo de la fila, ambas filas son de igual tamaño.
            fila2[i] += fila1[i] * coeficiente

# Método para dividir toda una fila entre un número. En este programa el divisor siempre será mayor a 0.
def dividirFila(fila, divisor):
    if (divisor != 1):              # Si el divisor es 1 no se realiza ninguna iteración.
        largo = len(fila)
        for i in range(largo):      # Se recorre el largo de la fila.
            fila[i] /= divisor


def simplex(tablaActual):
    minimo = min(tablaActual.matriz[0][:-1])
    if (minimo >= 0):

        tablaActual.numPivote = -1      # Se asignan estas variables a -1 para representar
        tablaActual.filaPivote = -1     # que son respuesta y ya no se iterará más.
        tablaActual.coluPivote = -1

        # Se comprueba si alguna variable artificial en las básicas
        if (any(elemento in tablaActual.actuales for elemento in tablaActual.artificiales)):
            tablaActual.estado = "Sin solución factible"

        # Se comprueba si las variables no básicas tienen 0
        elif (len(tablaActual.actuales) < tablaActual.matriz[0][:-1].count(0)):
            tablaActual.estado = "Soluciones múltiples"

        return [tablaActual]        # Se retorna la tabla.

    calcularColumnaPivote(tablaActual, minimo)              # Se calcula la columna pivote.

    listaPosiblesTablas = calcularFilaPivote(tablaActual)   # Se definen las tablas con posibles filas pivote.

    if (len(listaPosiblesTablas) == 0):         # Si no hay resultados es porque era no acotada.
        tablaActual.estado = "No acotada"
        listaTablas = [tablaActual]

    elif (len(listaPosiblesTablas) == 1):       # Si solo hay una se trabaja normal.
        operacionesGauss(listaPosiblesTablas[0])        # Se realizan las operaciones gauss.
        listaTablas = [tablaActual]
        listaTablas += simplex(listaPosiblesTablas[0])  # Se hace un llamado a simplex con el resultado.

    else:                                       # Si existen más de una es porque era degenerada.
        tablaActual.estado = "Degenerada"
        listaTablas = [tablaActual]
        #listaTablas = []
        maxTabla = None             # Se guarda la tabla con resultado final más grande.
        maxResultado = 0            # Se guarda el resultado más grande encontrado.

        for elemento in listaPosiblesTablas:    # Se opera con cada una de las tablas en la lista.
            #listaSimplexMedia = [MetodoSimplex.copiarTabla(elemento)]
            operacionesGauss(elemento)              # Se realizan las operaciones de Gauss.
            listaSimplexMedia = simplex(elemento)   # Se hace un llamado a simplex con el resultado.

            listaSimplexMedia[-1].numPivote = -1    # Se asignan estas variables a -1 para representar
            listaSimplexMedia[-1].filaPivote = -1   # que son respuesta y ya no se iterará más.
            listaSimplexMedia[-1].coluPivote = -1

            # Si no se ha guardado ningún resultado.
            if (maxTabla == None and listaSimplexMedia[-1].estado == "Normal"):
                maxTabla = listaSimplexMedia    # Se guarda la nueva tabla como máxima.
                maxResultado = maxTabla[-1].matriz[0][-1]

            # Si el resultado es mayor al que se tenía.
            elif (maxResultado < listaSimplexMedia[-1].matriz[0][-1] and listaSimplexMedia[-1].estado == "Normal"):
                listaTablas += maxTabla         # Se guarda la anterior en la lista de tablas.
                maxTabla = listaSimplexMedia    # Se guarda la nueva tabla como máxima.
                maxResultado = maxTabla[-1].matriz[0][-1]

            # Se almacena en la lista de tablas
            else:
                listaTablas += listaSimplexMedia

        # Se guarda la mayor en la lista de tablas
        listaTablas += maxTabla

    return listaTablas      # Se retorna la lista de tablas resultado.

# Función que realiza el cálculo de la columna pivote. Se utiliza el mínimo de la primera fila previamente calculado.
# Retorna la tabla con el dato resultante una vez encuentra el valor.
def calcularColumnaPivote(tablaActual, minimo):
    cantColumnas = len(tablaActual.matriz[0])       # Almacena el largo de la fila.
    for i in range(cantColumnas - 1):               # Se recorre la primera fila. No se recorre el último valor
                                                    # porque ahí se encuentra el lado derecho.
        if (tablaActual.matriz[0][i] == minimo):    # Si el valor en la columna i es igual al mínimo calculado
                                                    # se utiliza esta columna como pivote.
            tablaActual.coluPivote = i
            return tablaActual

# Método para definir la fila pivote. Además, identifica al número pivote.
# Retorna una lista de posibles tablas para continuar. La lista se encontrará vacia si se determina
# que la solución es no acotada. Si se determina que fuera degenerada se retorna una lista con todas
# las posibles tablas para continuar.
def calcularFilaPivote(tablaActual):
    minimo = -1                             # Variable que almacenará el menor valor calculado y factible.
    listaAContinuar = []                    # Lista donde se almacenarán las posibles tablas.
    cantFilas = len(tablaActual.matriz)     # Se almacena la cantidad de filas.
    for i in range(cantFilas - 1):          # Se recorre la fila menos el lado derecho de la misma.
        posiblePivote = tablaActual.matriz[i + 1][tablaActual.coluPivote]   # Se determina un posible número pivote.
        if (posiblePivote > 0):             # Si el posible pivote es mayor a 0 se continua.
            resultadoLadoDerecho = tablaActual.matriz[i + 1][-1] / posiblePivote    # Se calcula el resultado
                                                                                    # de dividir el lado derecho
                                                                                    # entre el pivote.
            if (minimo == -1):              # Si no se ha definido un mínimo.##############
                listaAContinuar = [i]       # Se define i como posible fila pivote.
                minimo = resultadoLadoDerecho       # Se almacena el resultado para posteriores calculos.

            elif (minimo > resultadoLadoDerecho):   # Si se encuentra otro valor menor al actualmente almacenado
                listaAContinuar = [i]               # Se define i como posible fila pivote.
                minimo = resultadoLadoDerecho       # Se almacena el resultado para posteriores calculos.

            elif (minimo == resultadoLadoDerecho):  # Se comprueba si hay degeneración.
                listaAContinuar.append(i)           # Se almacena el nuevo valor para la fila pivote.

            # Si el resultado fuera mayor no se hace nada.

    listaPosiblesTablas = []                # Lista que almacenará los resultados.

    for elemento in listaAContinuar:        # Por cada fila pivote se crea una tabla y se definen sus valores.
        tablaActual.filaPivote = elemento
        tablaActual.numPivote = tablaActual.matriz[elemento + 1][tablaActual.coluPivote]
        tablaNueva = MetodoSimplex.copiarTabla(tablaActual)
        listaPosiblesTablas.append(tablaNueva)      # Se guarda la tabla en la lista de tablas.

    return listaPosiblesTablas              # Se retorna la lista resultante.

# Función para realizar las operaciones de Gauss para dejar a la columna pivote con solo el valor 1 en la
# posición de la fila pivote. Se realizan por cada tabla en el simplex.
def operacionesGauss(tablaActual):
    filaPivoteActual = tablaActual.filaPivote   # Variable que almacena la fila pivote.
    coluPivoteActual = tablaActual.coluPivote   # Variable que almacena la columna pivote.
    numPivote = tablaActual.numPivote           # Variable que almacena el número pivote.

    tablaActual.actuales[filaPivoteActual] = coluPivoteActual           # Se le indica a la lista de actuales que
                                                                        # cambia su valor por el de la columna pivote,
                                                                        # se le suma 1 para que sea más comprensible al
                                                                        # usuario ya que en el programa se inicia en 0.

    dividirFila(tablaActual.matriz[filaPivoteActual + 1], numPivote)    # Se divide toda la fila por el número pivote.

    operaEntreFilas(tablaActual.matriz[filaPivoteActual + 1], tablaActual.matriz[0],    # Se realizan las operaciones
                    -1 * tablaActual.matriz[0][coluPivoteActual])                       # en la fila 0.

    cantFilas = len(tablaActual.matriz)
    for i in range(1,cantFilas):              # Se realizarán las operaciones para el resto de filas.
        if (tablaActual.actuales[i-1] != coluPivoteActual):
            operaEntreFilas(tablaActual.matriz[filaPivoteActual + 1], tablaActual.matriz[i],
                            -1 * tablaActual.matriz[i][coluPivoteActual])

    return tablaActual