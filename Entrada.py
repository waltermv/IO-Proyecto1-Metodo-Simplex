# Clase utilizada para leer los problemas desde una archivo, lee los valores del archivo y los almacena en tipos de datos faciles de manipular
class Entrada:
    # Construcctor de la clase recibe el nombre del archivo que se va a leer
    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo # atributo para el nombre del archivo
        self.metodo = None  # atributo para el metodo a utilizar 0, 1 o 2 para simplex, gran m o dos faces.
        self.optimizacion = None # atributo para el tipo de optimización maximización o minimización
        self.cantidadVariablesDecision = None # atributo para la cantidad de variable de desición
        self.cantidadRestricciones = None # atributo para la cantidad de restricciones
        self.tabla = [] # Matriz donde se inrgesaran los valores del archivo
        self.restriccion = [] # Lista con el tipo de restrición (<=, >= o =) de cada fila

    # Metodo para leer el archivo de entrada
    def leerEntrada(self):
        archivo = open(self.nombreArchivo) # Se abre el archivo para poder acceder a el
        self.metodo, self.optimizacion, self.cantidadVariablesDecision, self.cantidadRestricciones = archivo.readline().split(
            ",")    # Se lee la primer linea se optiene el metodo, tipo de optimización, la cantidad de variables de decisión y la cantidad de restricciones
        self.metodo = int(self.metodo) # Se castea el valor a entero
        self.cantidadVariablesDecision = int(self.cantidadVariablesDecision) # Se castea el valor a entero
        self.cantidadRestricciones = int(self.cantidadRestricciones) # Se castea el valor a entero
        temp = [0] * (self.cantidadVariablesDecision + 1) # Lista temporal para asignar los valores que se leen
        coeficientes = list(map(float, archivo.readline().split(","))) # Se lee la primer linea, los valores pueden ser enteros o flotantes
        if self.optimizacion == "max": # Si el tipo de problema es de maximización
            coeficientes = [x * -1 for x in coeficientes] # Se multiplica por -1
        for i in range(len(coeficientes)):
            temp[i] = float(coeficientes[i]) # Se pasan los valores a la lista temporal
        self.tabla.append(temp) # Se añade los valores de la función objetivo a la matriz

        #Se ingresan las restricciones
        for i in range(self.cantidadRestricciones): # Se itera por la cantidad de restricciones
            coeficientes = archivo.readline().split(",") # Se lee la linea y se divide por comas
            temp = [0] * (self.cantidadVariablesDecision + 1) # Establemos temp como una lista de ceros
            self.restriccion.append(coeficientes.pop(len(coeficientes) - 2)) # En la penultima posición extraemos el tipo de restricción y se añade a la lista de restricciones
            for j in range(len(coeficientes)):
                temp[j] = float(coeficientes[j]) # Se pasan los valores leidos a temp
            self.tabla.append(temp) # Se agrega la lista de la restricción a la tabla
        archivo.close() # Se cierra el archivo
