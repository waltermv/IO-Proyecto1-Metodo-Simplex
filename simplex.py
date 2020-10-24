import sys

from fractions import Fraction
from Entrada import *
from MetodoSimplex import *
from MetodoDosFases import *
from MetodoGranM import *
from Salida import *


def imprime(respuesta):
    for i in range(len(respuesta)):
        for j in range(len(respuesta[i].matriz)):
            #print([str(Fraction(x)) for x in respuesta[i].matriz[j]])
            print(respuesta[i].matriz[j])
        # print(respuesta[i].numPivote)
        print("Fila", respuesta[i].filaPivote)
        print("Columna", respuesta[i].coluPivote)
        print("Pivote", respuesta[i].numPivote)
        print("Estado", respuesta[i].estado)
        print("Iteración", respuesta[i].contador)
        print("Actuales", respuesta[i].actuales)
        print("-------------------------------")


def ayuda():
    print("Información de Ayuda")


def resolverSimplex(entrada):
    if not ("=" in entrada.restriccion or ">=" in entrada.restriccion):
        problema = MetodoSimplex()
        problema.cargar(entrada)
        respuesta = simplex(problema)
        return respuesta
    else:
        sys.exit("No es posible solucionar mediante el metodo simplex")


def resolverDosFases(entrada):
    # print(entrada.tabla)
    problema = MetodoDosFases()
    problema.cargar(entrada)
    problema.primeraFase()
    primeraFase = simplex(problema)
    primeraFase2 = [MetodoSimplex(x.matriz, x.actuales, x.artificiales, x.contador, x.estado, x.numPivote, x.filaPivote, x.coluPivote) for x in primeraFase]
    # imprime(primeraFase)
    problema.segundaFase(MetodoSimplex.copiarTabla(primeraFase[-1]), entrada.tabla[0])
    segundaFase = simplex(problema)
    imprime(primeraFase2)
    print("AAAAAAA--------------------------------------------------AAAAAAAAAAAA")
    imprime(segundaFase)
    return [primeraFase2, segundaFase]


def resolverGranM(entrada):
    problema = MetodoGranM()
    problema.cargar(entrada)
    respuesta = problema.resolver(entrada.optimizacion)
    imprime(respuesta)
    return respuesta

def selecionarMetodo(entrada):
    if entrada.metodo == 0:
        return resolverSimplex(entrada)
    elif entrada.metodo == 1:
        return resolverGranM(entrada)
    elif entrada.metodo == 2:
        return resolverDosFases(entrada)
    else:
        sys.exit("Error - metodo desconocido")


def main(args):
    if len(args) == 3 and args[1] == "[-h]":
        ayuda()
    elif len(args) == 2:
        archivoEntrada = Entrada(args[1])
        archivoEntrada.leerEntrada()
        resultado = selecionarMetodo(archivoEntrada)
        archivoSalida = Salida(archivoEntrada, resultado)
        archivoSalida.escribirArchivo()
    else:
        sys.exit("Error - Entrada invalida")


if __name__ == '__main__':
    main(sys.argv)
