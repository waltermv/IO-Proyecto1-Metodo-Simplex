# Clase utilizada para imprimir el resultado del
class Salida:
    # Constructor de la clase, recibe un objeto de tipo entrada y un objeto MetodoSimplex
    def __init__(self, entrada, listaTablas):
        self.entrada = entrada  # Establece el atributo entrada
        self.listatablas = listaTablas  # Establece el atributo listatablas, que son la lista de tablas del problema
        self.cantidadVar = entrada.cantidadVariablesDecision + (entrada.restriccion.count("<=") + entrada.restriccion.count("=") + (2 * entrada.restriccion.count(">=")))   # Suma la cantidad de columnas del problema
        self.variables = []  # Atributo que posteriormente se utilizara
        self.actuales = []  # Atributo que posteriormente se utilizara

    # Metodo para escribir el resultado en un archivo, crea un archivo de salida, selecciona el tipo de metodo para llamar a otro metodo encargado de llenar el archivo
    def escribirArchivo(self):
        archivo = open(self.entrada.nombreArchivo[:-4] + "_solution.txt", "w")  #Crea el archivo de salidad
        if self.entrada.metodo == 0: # Si el metodo es simplex
            archivo.write("Resultado utilizando Metodo Simplex:\n") # Escribe en el archivo
            self.escribirSimplex(archivo, self.listatablas) # Llama a otro método para imprimir el resultado en el archivo
            self.escribirResultado(self.listatablas[-1], archivo) # Llama al metodo para imprimir en consola la iteración
        elif self.entrada.metodo == 1: # Si el metodo es gran m
            self.escribirGranM(archivo, self.listatablas)   # Llama a otro método para imprimir el resultado en el archivo
            self.escribirResultado(self.listatablas[-1], archivo)   # Llama al metodo para imprimir en consola la iteración
        elif self.entrada.metodo == 2: # Si el metodo es dos fases
            self.escribirDosFases(archivo, self.listatablas[0], self.listatablas[1]) # Llama al metodo para imprimir en consola la iteración
        archivo.close() # Se cierra el archivo

    # Método para escribir en archivo problemas de dos fases
    def escribirDosFases(self, archivo, primeraFase, segundaFase):
        archivo.write("Resultado utilizando Metodo de Dos Fases: \n") # Escribe en el archivo
        archivo.write("Primera Fase: \n") # Escribe en el archivo
        self.listatablas = primeraFase # Asigna el atributo listaTablas
        self.escribirSimplex(archivo, primeraFase) # Escribe en el archivo la primera fase
        archivo.write("\n") # Escribe un salto de linea
        archivo.write("Segunda Fase: \n") # Escribe en el archivo
        self.cantidadVar = len(segundaFase[0].matriz[0]) - 1 # Asigna el atributo cantidad de variables, se eliminan las de artificiales
        self.listatablas = segundaFase  # Asigna el atributo listatablas para la segunda face
        self.escribirSimplex(archivo, segundaFase)  # Escribe en el archivo la segunda fase
        self.escribirResultado(segundaFase[-1], archivo)    # Escribe en el archivo el resultado

    # Método para escribir en archivo problemas de gran m
    def escribirGranM(self, archivo, listaTablas):
        archivo.write("Resultado utilizando Metodo de la Gran M:") # Escribe en el archivo
        self.escribirSimplex(archivo, listaTablas)   # Escribe en el archivo la gran m

    # Método para escribir en archivo problemas de método simplex
    def escribirSimplex(self, archivo, listaTablas):
        variables = ["VB"] + ["X" + str(elemento) for elemento in range(self.cantidadVar)] + ["LD"] # Crea la lista de variables, la primera fila
        matriz = [] # Matriz para guardarar los resultados dandoles formato para imprimir
        actuales = [] # Lista de las variables basicas
        lista = [] # Lista de las matrices ahora con los atributos para imprimir
        for elemento in self.listatablas: # Iteramos las diferentes tablas generadas
            actuales = ["U"] + elemento.actuales # Creamos la lista de las vb
            matriz.append(variables.copy()) # Ingresamos una copia de la lista de variables
            for i in range(len(elemento.matriz)): # Iteramos las filas para darles formato
                matriz.append([actuales[i]] + elemento.matriz[i]) # Se agrega a la matriz temporal la nueva fila
            lista.append(matriz) # Se agrega a la lista
            variables[elemento.coluPivote] = "X" + str(actuales[elemento.filaPivote]) # Se actualiza la lista de variables
            matriz = [] # Se limpia la matriz temporal
        lista[-1][0][0] = "VB"
        for elemento in range(len(lista)): # Se itera la nueva lista con las tabls modificadas para imprimir
            estado = self.listatablas[elemento].contador
            archivo.write("Iteración: " + str(estado) + "\n") # Escribe en el archivo
            # print("Iteración: " + str(estado))
            for i in range(len(lista[elemento])): # Itera las filas de la matriz
                for j in range(len(lista[elemento][0])): # Itera las columna
                    # print(f"{lista[elemento][i][j]:<20}", end=" ")
                    archivo.write(f"{lista[elemento][i][j]:<20}") # Escribe en el archivo
                # print()
                archivo.write("\n") # Escribe en el archivo un salto de linea
            if self.listatablas[elemento].coluPivote != -1: # Si el valor de la columna pivot es -1, significa que llego a un estado final
                archivo.write((f"VB entrante: X{self.listatablas[elemento].coluPivote}, VB saliente: X{self.listatablas[elemento].filaPivote}, Número Pivot: {self.listatablas[elemento].numPivote}\n")) # Si no es -1 entonces imprime la variable entrante y saliente y el elemento pivot
                # print(f"VB entrante: X{self.listatablas[elemento].coluPivote}, VB saliente: X{self.listatablas[elemento].filaPivote}, Número Pivot: {self.listatablas[elemento].numPivote}")
            archivo.write("________________________________________" * len(lista[elemento])) # Imprime un divisor de tablas
            archivo.write("\n") # Escribe en el archivo un salto de linea
            # print("________________________________________" * len(lista[elemento]))
        self.variables = variables  # Actualiza el valor de los atributos
        self.actuales = actuales    # Actualiza el valor de los atributos

    # Escribir el resultado final en el archivo el valor de U y las variables
    def escribirResultado(self, elemento, archivo):
        respuesta = [] # Lista de los valores de las variables
        for i in range(self.cantidadVar):
            if i in elemento.actuales: # Si la variable esta dentro las actuables
                respuesta.append(elemento.matriz[elemento.actuales.index(i) + 1][-1]) # Ingresa el valor en la ultima columna en la fila en donde se encuentra la vb
            else: # Sino
                respuesta.append(0) # Ingresa un 0

        variables = self.variables  # Lista temporal
        matriz = [] # Lista temporal
        actuales = self.actuales    # Lista temporal
        variables = self.variables  # Lista temporal
        lista = []  # Lista temporal
        for elemento in self.listatablas: # Se realiza lo mismo para imprimir la ultima tabla que para escribir en el archivo
            actuales = ["U"] + elemento.actuales
            matriz.append(variables.copy())
            for i in range(len(elemento.matriz)):
                matriz.append([actuales[i]] + elemento.matriz[i])
            lista.append(matriz)
            variables[elemento.coluPivote] = "X" + str(actuales[elemento.filaPivote])
        for i in range(len(matriz)): # Ahora en lugar de escribir en el archivo imprime en colsola
            for j in range(len(matriz[0])):
                print(f"{matriz[i][j]:<20}", end=" ")
            print()
        # Se calcula el valor de U y las variables
        if elemento.coluPivote != -1:  # Si es -1, no se imprime lo siguiente
            print(
                f"VB entrante: X{self.listatablas[elemento].coluPivote}, VB saliente: X{self.listatablas[elemento].filaPivote}, Número Pivot: {self.listatablas[elemento].numPivote}")
        print()
        # Si un proble es de minimización es necesario multiplicarlo por -1 a los resultados finales
        if self.entrada.optimizacion == "min": # Si el valor de optimización es min
            respuesta = [-x for x in respuesta] # Asigna a los valores negativos
            archivo.write(f"Estado: {elemento.estado}\n") # Escribe en el archivo
            print(f" Estado: {elemento.estado}\n") # Imprime en consola
            archivo.write(f" Respuesta final:    U = {-elemento.matriz[0][-1]} {respuesta}")    # Escribe el resultado final
            print(f" Respuesta final:    U = {-elemento.matriz[0][-1]} {respuesta}")    # Imprime el resultado final
        else: # Sino
            archivo.write(f"Estado: {elemento.estado}\n") # Escribe en el archivo
            print(f" Estado: {elemento.estado}\n")  # Imprime en consola
            archivo.write(f" Respuesta final:   U = {elemento.matriz[0][-1]} {respuesta}")  # Escribe el resultado final
            print(f" Respuesta final:    U = {elemento.matriz[0][-1]} {respuesta}") # Imprime el resultado final