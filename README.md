# Investigación de Operaciones - Primer Proyecto: Método Simplex
Primer proyecto del curso de Investigación de Operaciones (código ic-6400) en la carrera de Ingeniería en Computación del Tecnológico de Costa Rica.

## Objetivo

El objetivo es demostrar la comprensión del algoritmo del Método Simplex para resolver problemas de maximización y minimización de programación lineal.

## Requerimientos

* El programa recibe el nombre de un archivo, tal archivo contiene los parámetros de un problema de Programación Lineal (se describe más adelante). El programa debe calcular el resultado óptimo, los resultados de la respuesta final deben ser desplegados en la consola, el resultado completo con las tablas intermedias deben ser guardas en el archivo de salida con el sufijo _solution.txt.

* En el archivo de salida la solución debe desplegar el estado de los resultados intermedios en cada iteración, lo que significa guardar la tabla inicial y las tablas temporales al final de cada iteración así como los valores del reglón pivot, columna pivot y el número pivot.

* El programa debe implementar las 3 formas de las restricciones: <=, =, >=. Usando las de variables de holgura, las variables de exceso y las variables artificiales. Usando el Método de la Gran M y el Método de las 2 Fase según se le indique en el archivo de entrada (se describe más adelante).

* El programa debe ser capaz de reconocer las soluciones múltiples, cuando la solución es degenerada, cuando la solución no esta acotada, y cuando no existe solución factible. Todo esto imprimiendo un mensaje en consola y el archivo de salida donde indique todos los valores que considere necesarios para explicar la situación.

* La ejecución del programa se hará por linea de comandos, y debe respetar el formato establecido, sin excepción alguna, si no es respetado se descontaran puntos.

## Funcionamiento del programa

A continuación se muestra el comando para la ejecución del programa. El parámetro h es opcional y es utilizado para mostrar información sobre el uso del programa. 

```console
python simplex.py [-h] archivo.txt
```
La estructura del archivo de entrada es la siguiente: 

`Método, Optimización, Número de variables de decisión, Número de restricciones coeficientes de la función objetivo coeficientes de las restricciones y Signo de restricción`

Donde método es un valor numérico \[ 0=Simplex, 1=GranM, 2=DosFases \]. Por su parte, la optimización se indica con "min" o "max".

Ejemplo del funcionamiento:

![2021-08-13_20-13](https://user-images.githubusercontent.com/56206208/129431424-63392edc-e470-4395-8c2b-0fef993dfe92.png)

## Estado

El programa funciona correctamente, todas las funcionalidades fueron correctamente implementadas.

## Realizado por:

* Brandon Ledezma Fernández

* Walter Morales Vásquez
