# Clase que representa una tabla utilizada para la realización del método Simplex.
class Tabla:
	# Método constructor de la clase.
	def __init__(self, matriz, actuales, artificiales=[], contador=0, estado="Normal", numPivote=0, filaPivote=0, coluPivote=0):
		self.matriz = matriz			# La matriz en la que se colocarán los valores de las ecuaciones.
		self.actuales = actuales		# Lista que indica cuales variables se encuentran como variables básicas.
		self.artificiales = artificiales	# Lista que indica cuales variables son artificiales.
		self.contador = contador		# Contador que cuenta el número de tabla.
		self.estado = estado			# Variable que indica el estado actual de la tabla
										# entre "Normal", "Degenerada", "No acotada",
										# "Soluciones múltiples" o "Sin solución factible"
		self.numPivote = numPivote		# Variable que representa el número pivote actual.
		self.filaPivote = filaPivote	# Almacena el valor de la fila pivote.
		self.coluPivote = coluPivote	# Representa la posición de la columna pivote.
 
	#Método para crear una nueva tabla a partir de una ya existente.
	@classmethod
	def copiarTabla(cls, tablaC):
		matriz = [fila[:] for fila in tablaC.matriz]	# Se copia la matriz existente, se hace de esta.
														# forma porque normalmente se pasaría por referencia.
		actuales = tablaC.actuales[:]					# Se copia la lista de variables básicas.
		artificiales = tablaC.artificiales[:]			# Se copia la lista de variables artificiales.
		contador = tablaC.contador + 1					# Se utiliza el mismo contador pero aumentado en 1.
		estado = "Normal"								# Se copia el estado anterior.
		numPivote = tablaC.numPivote					# Se guarda el número pivote anterior
		filaPivote = tablaC.filaPivote 					# Se almacena el valor de la fila pivote.
		coluPivote = tablaC.coluPivote					# Se almacena el valor de la columna pivote.
		return cls(matriz, actuales, artificiales,		# Se retorna la nueva tabla.
		contador, estado, numPivote, filaPivote, coluPivote)
 
def operaEntreFilas(fila1, fila2, coeficiente):
	if(coeficiente != 0):
		largo = len(fila1)
		for i in range (largo):
			fila2[i] = fila1[i] * coeficiente + fila2[i]
 
def dividirFila(fila, divisor):
	if(divisor != 1):
		largo = len(fila)
		for i in range (largo):
			fila[i] = fila[i] / divisor
 
def simplex(tablaActual):
	minimo = min(tablaActual.matriz[0])
	if(minimo >= 0):
		if(len(tablaActual.actuales) < tablaActual.matriz[0][:-1].count(0)):	# Se comprueba si las variables no básicas tienen 0
			tablaActual.estado = "Soluciones múltiples"
		elif(any(elemento in tablaActual.actuales for elemento in tablaActual.artificiales)):	# Se comprueba si alguna variable artificial
			tablaActual.estado = "Sin solución factible"										# está entre las básicas
		return [tablaActual]
 
	calcularColumnaPivote(tablaActual, minimo)
 
	listaPosiblesTablas = calcularFilaPivote(tablaActual)
	
	if(len(listaPosiblesTablas) == 0):
		tablaActual.estado = "No acotada"
		listaTablas = [tablaActual]
 
	elif(len(listaPosiblesTablas) == 1):
		operacionesGauss(listaPosiblesTablas[0])
		listaTablas = [tablaActual]
		listaTablas += simplex(listaPosiblesTablas[0])
 
	else:
		tablaActual.estado = "Degenerada"
		listaTablas = [tablaActual]
		maxTabla = None
		maxResultado = 0
		for elemento in listaPosiblesTablas: # Operaciones para dejar a la de mayor resultado de último.
			
			operacionesGauss(elemento)
			listaSimplexMedia = simplex(elemento)
 
			if(maxTabla == None):			# And estado es "Normal"?
				maxTabla = listaSimplexMedia
				maxResultado = maxTabla[-1].matriz[0][-1]
 
			elif(maxResultado < listaSimplexMedia[-1].matriz[0][-1]):
				listaTablas += maxTabla
				maxTabla = listaSimplexMedia
				maxResultado = maxTabla[-1].matriz[0][-1]
 
			else:
				listaTablas += listaSimplexMedia
				
		listaTablas += maxTabla
		
	return listaTablas
 
def calcularColumnaPivote(tablaActual, minimo):
	#Calculo columna pivote
	cantColumnas = len(tablaActual.matriz[0])
	for i in range (cantColumnas-1):
		if(tablaActual.matriz[0][i] == minimo):
			tablaActual.coluPivote = i
			return tablaActual
 
def calcularFilaPivote(tablaActual):
	#Calculo fila pivote
	minimo = -1
	listaAContinuar = []
	cantFilas = len(tablaActual.matriz)
	for i in range (cantFilas-1):
		posiblePivote = tablaActual.matriz[i+1][tablaActual.coluPivote]
		if(posiblePivote > 0):
			resultadoLadoDerecho = tablaActual.matriz[i+1][-1] / posiblePivote
			if(minimo == -1):
				listaAContinuar = [i]
				minimo = resultadoLadoDerecho
			elif(minimo > resultadoLadoDerecho):
				listaAContinuar = [i]
				minimo = resultadoLadoDerecho
			elif(minimo == resultadoLadoDerecho): # Se comprueba si hay degeneración
				listaAContinuar.append(i)
				
	listaPosiblesTablas = []
 
	for elemento in listaAContinuar:
		tablaNueva = Tabla.copiarTabla(tablaActual)
		tablaNueva.filaPivote = elemento
		tablaNueva.numPivote = tablaActual.matriz[elemento+1][tablaActual.coluPivote]
		listaPosiblesTablas.append(tablaNueva)
 
	return listaPosiblesTablas
 
def operacionesGauss(tablaActual):
	#Operaciones
	filaPivoteActual = tablaActual.filaPivote	#Variables para hacer más legible el código
	coluPivoteActual = tablaActual.coluPivote
	numPivote = tablaActual.numPivote
 
	tablaActual.actuales[filaPivoteActual] = coluPivoteActual + 1
	dividirFila(tablaActual.matriz[filaPivoteActual+1], numPivote)
 
	operaEntreFilas(tablaActual.matriz[filaPivoteActual+1], tablaActual.matriz[0], -1*tablaActual.matriz[0][coluPivoteActual])
 
	cantFilas = len(tablaActual.matriz)
	for i in range (cantFilas-1):
		if(tablaActual.actuales[i] != coluPivoteActual+1):
			operaEntreFilas(tablaActual.matriz[filaPivoteActual+1], tablaActual.matriz[i+1], -1*tablaActual.matriz[i+1][coluPivoteActual])
 
	return tablaActual

