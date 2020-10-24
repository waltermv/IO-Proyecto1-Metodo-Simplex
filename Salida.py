class Salida:
    def __init__(self, entrada, listaTablas):
        self.entrada = entrada
        self.listatablas = listaTablas
        self.cantidadVar = entrada.cantidadVariablesDecision + (entrada.restriccion.count("<=") + entrada.restriccion.count("=") + (2 * entrada.restriccion.count(">=")))
        self.variables = ["U"] + ["X" + str(elemento) for elemento in range(self.cantidadVar)] + ["LD"]
        self.actuales = ["U"] + ["X"] * entrada.cantidadRestricciones

    def escribirArchivo(self):
        archivo = open(self.entrada.nombreArchivo[:-4] + "_solution.txt", "w")
        if self.entrada.metodo == 0:
            archivo.write("Resultado utilizando Metodo Simplex:\n")
            self.escribirSimplex(archivo, self.listatablas)
        elif self.entrada.metodo == 1:
            self.escribirGranM(archivo, self.listatablas)
        elif self.entrada.metodo == 2:
            self.escribirDosFases(archivo, self.listatablas[0], self.listatablas[1])
        archivo.close()

    def escribirDosFases(self, archivo, primeraFase, segundaFase):
        archivo.write("Resultado utilizando Metodo de Dos Fases: \n")
        archivo.write("Primera Fase: \n")
        self.listatablas = primeraFase
        self.escribirSimplex(archivo, primeraFase)
        archivo.write("\n")
        archivo.write("Segunda Fase: \n")
        # print(segundaFase)
        self.cantidadVar = len(segundaFase[0].matriz[0]) - 1
        self.listatablas = segundaFase
        self.escribirSimplex(archivo, segundaFase)

    def escribirGranM(self, archivo, listaTablas):
        archivo.write("Resultado utilizando Metodo de la Gran M:")
        self.escribirSimplex(archivo,listaTablas)

    def escribirSimplex(self, archivo, listaTablas):
        variables = ["VB"] + ["X" + str(elemento) for elemento in range(self.cantidadVar)] + ["LD"]
        matriz = []
        lista = []
        for elemento in self.listatablas:
            actuales = ["U"] + elemento.actuales
            matriz.append(variables.copy())
            for i in range(len(elemento.matriz)):
                matriz.append([actuales[i]] + elemento.matriz[i])
            lista.append(matriz)
            variables[elemento.coluPivote] = "X" + str(actuales[elemento.filaPivote])   # todo resolver si es -1
            matriz = []
        lista[-1][0][0] = "VB"
        for elemento in range(len(lista)):
            estado = self.listatablas[elemento].contador
            archivo.write("Iteración: " + str(estado) + "\n")
            print("Iteración: " + str(estado))
            for i in range(len(lista[elemento])):
                for j in range(len(lista[elemento][0])):
                    print(f"{lista[elemento][i][j]:<20}", end=" ")
                    archivo.write(f"{lista[elemento][i][j]:<20}")
                print()
                archivo.write("\n")
            archivo.write((f"VB entrante: X{self.listatablas[elemento].coluPivote}, VB saliente: X{self.listatablas[elemento].filaPivote}, Número Pivot: {self.listatablas[elemento].numPivote}\n"))
            print(f"VB entrante: X{self.listatablas[elemento].coluPivote}, VB saliente: X{self.listatablas[elemento].filaPivote}, Número Pivot: {self.listatablas[elemento].numPivote}")
            archivo.write("________________________________________" * len(lista[elemento]))
            archivo.write("\n")
            print("________________________________________" * len(lista[elemento]))
