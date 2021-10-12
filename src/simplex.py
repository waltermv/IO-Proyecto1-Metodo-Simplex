import sys

from fractions import Fraction
from Entrada import *
from MetodoSimplex import *
from MetodoDosFases import *
from MetodoGranM import *
from Salida import *

# Función utilizada para imprimir el consola una descripción de como usar el programa,
# parámetros y formato de archivo de entrada.
def ayuda():
    print("Programa para solucionar problemas del Método Simplex")
    print("Este programa esta desarrollado en el lenguaje de programación")
    print("Para utilizar este programa es necesario incluir parametros especificos")
    print("Para ejecutar el programa se deje ejecutar:")
    print("\t\tpython simplex.py archivo.txt")
    print("Donde archivo.txt es el nombre del archivo que contiene el archivo el cual debe tener como formato:")
    print("método, optimización, Número de variables de decisión, Número de restricciones\ncoeficientes de la función objetivo\ncoeficientes de las restricciones y signo de restricción")
    print("Ejemplo de entrada:")
    print("El problema es: \n \t Min U = 3x1 + 5x2\n\t 2x1 + x2 ≤ 6\n\t -x1 + 3x2 = 9\n\t x2 ≥ 4")
    print("Formato del archivo:\n\t 1,min,2,3\n\t 3,5\n\t 2,1,<=,6\n\t -1,3,=,9\n\t 0,1,>=,4")
    print("El programa gerenará un archivo con la solución con subfijo '_solution.txt'")
    print()


# Función para asignar los problemas de tipo simplex
def resolverSimplex(entrada):
    if not ("=" in entrada.restriccion or ">=" in entrada.restriccion): # Si no se encuentra un '=' o '>='
        problema = MetodoSimplex() # Se crea un objeto MetodoSimplex
        problema.cargar(entrada) # Se carga la entrada del archivo
        respuesta = simplex(problema) # Se realiza el algoritmo del simplex
        return respuesta
    else: # No es posible solucionar el problema
        sys.exit("No es posible solucionar mediante el metodo simplex")

# Función para asignar los problemas de tipo dos fases
def resolverDosFases(entrada):
    problema = MetodoDosFases() # Se crea un objeto de MetodoDosFases
    problema.cargar(entrada)    # Se carga la entrada del archivo
    problema.primeraFase()  #Se realizar los cambioas para la primera fase
    primeraFase = simplex(problema) # Se realiza la primera etapa
    primeraFase2 = [MetodoSimplex(x.matriz, x.actuales, x.artificiales, x.contador, x.estado, x.numPivote, x.filaPivote,
                                  x.coluPivote) for x in primeraFase] # Se hace una copia de la matriz, porque posteriormente hay un problema de referencia
    problema.segundaFase(MetodoSimplex.copiarTabla(primeraFase[-1]), entrada.tabla[0])  # Se realizan los cambios para ejecutar la segunda fase
    segundaFase = simplex(problema) # Se realiza la segunda fase
    return [primeraFase2, segundaFase]


def resolverGranM(entrada):
    problema = MetodoGranM() # Se crea un objeto de tipo gran m
    problema.cargar(entrada)    # Se carga la entrada del archivo
    respuesta = problema.resolver(entrada.optimizacion) # Resuelve el problema de la gran m
    return respuesta

# Función que se encarga de llamara a las funciones correctar para solucionar los problemas
def selecionarMetodo(entrada):
    if entrada.metodo == 0:
        return resolverSimplex(entrada)
    elif entrada.metodo == 1:
        return resolverGranM(entrada)
    elif entrada.metodo == 2:
        return resolverDosFases(entrada)
    else:
        sys.exit("Error - metodo desconocido")

# Función main
def main(args):
    if len(args) == 3 and args[1] == "[-h]": # Si los argumentos es [-h] archivo.txt
        ayuda() # Se imprime la ayuda
        archivoEntrada = Entrada(args[2]) # Se lee el archivo
        archivoEntrada.leerEntrada() # Se manipula la entrada
        resultado = selecionarMetodo(archivoEntrada) # Se realiza el algoritmo
        archivoSalida = Salida(archivoEntrada, resultado) # Se genera la respuesta
        archivoSalida.escribirArchivo() # Se escribe en el archivo
    elif len(args) == 2 and args[1] != "[-h]": # Si los argumentos son archivo.txt
        archivoEntrada = Entrada(args[1])  # Se lee el archivo
        archivoEntrada.leerEntrada()  # Se manipula la entrada
        resultado = selecionarMetodo(archivoEntrada)  # Se realiza el algoritmo
        archivoSalida = Salida(archivoEntrada, resultado)  # Se genera la respuesta
        archivoSalida.escribirArchivo()  # Se escribe en el archivo
    elif args[1] == "[-h]": # Si el [-h]
        ayuda() # Se imprime la ayuda
    else:  #Sino
        sys.exit("Error - Entrada invalida") # Se finaliza el programa


if __name__ == '__main__':
    main(sys.argv)
