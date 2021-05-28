import os
from colorama import init, Fore
import time
import sys
import re
from tabulate import tabulate
from shutil import rmtree


def saludo():
	re = """
	*******      
	*      * 
	*      *   **  ******     *         *     *  ******     *         **  ******    ********
	*      *   **  *     *    * *****   *     *  *     *    * *****   **  *      *  *      *
	********   **  *      *   **     *  *     *  *      *   **     *  **  *      *  *      *
	*       *  **  *********  *      *   *   *   *********  *      *  **  *      *  *      *
	*       *  **  *          *      *    * *    *          *      *  **  *      *  *      *
	*       *  **  *          *      *    * *    *          *      *  **  *      *  *      *
	*********  **   *******   *      *     *      *******   *      *  **  ******    ********
	"""
	return re





class Main:

	def __init__(self, pathNow):
		init(autoreset = True) # -> Inicializamos colorama
		print(saludo())
		print("\n")
		time.sleep(0.25)
		os.system("cls")

		self.__colorFg = Fore.LIGHTWHITE_EX

		self.__comandosUsados = []

		self.__path_now = pathNow
		self.__contadorDeRutas = 1

		self.__inicio()


	def __inicio(self):
		print(Fore.LIGHTMAGENTA_EX + "[{}]".format(self.__contadorDeRutas) + Fore.LIGHTGREEN_EX + " = {}".format(self.__path_now))
		self.__comandoL = input(self.__colorFg + "\nζ ")


		# --- Comando para salir del cmd --- #
		if self.__comandoL == "gb":
			print("Adios")
			sys.exit()


		# -- Comando para ingresar a un directorio --- #
		elif re.match("exp (.+)", self.__comandoL):
			# Le pasamos solo el nombre de la carpeta, ya que el comando ya lo sabemos
			# hacemos una lista con la cadena, donde el [0] = comando, [1] = carpeta
			self.__agregarComando(self.__comandoL)
			self.__exp(self.__comandoL.split(' ')[1])


		# --- Comando para salir de un directorio --- #
		elif re.match("ex \d", self.__comandoL):
			# Este método funciona de la siguiente forma:
			# ex n
			# donde n es el numero de directorios que quiere retroceder
			# al minimo directorio es "C:"

			# Aplicamos la misma lógica del comando de arriba
			self.__agregarComando(self.__comandoL)
			self.__ex( int(self.__comandoL.split(' ')[1]) )


		# --- Comando para limpiar pantalla --- #
		elif self.__comandoL == "lim":
			self.__agregarComando(self.__comandoL)
			os.system("cls")
			self.__inicio()


		# --- Comando para ver files de un dir --- #
		elif self.__comandoL == "df":
			self.__agregarComando(self.__comandoL)
			self.__verArchivos()


		# --- Comando para crear archivos/carpetas --- #
		elif re.match("cr [a-z]", self.__comandoL):
			self.__agregarComando(self.__comandoL)
			self.__copia = self.__comandoL.strip() # -> Le quitamos los espacios a lo que escribio
			self.__crearArchivo(self.__copia[3:])# -> Le mandamos lo siguiente ~cr~ file.extension


		# --- Comando ara borrar archivos/carpetas --- #
		elif re.match("br [a-z]", self.__comandoL):
			self.__agregarComando(self.__comandoL)
			self.__copia = self.__comandoL.strip()  # -> Le quitamos los espacios a lo que escribio
			self.__borrar(self.__copia[3:])  # -> Le madamos solo el nombre ~br~ <nombre>


		# --- Comando para renombrar archvivos/carpetas ---#
		elif re.match("rnm [a-z]", self.__comandoL):
			self.__agregarComando(self.__comandoL)
			self.__copia = self.__comandoL.strip()  # -> Le quitamos los espacios a lo que escribio
			self.__renombrar(self.__copia[4:])  # -> Le madamos solo el nombre ~rnm~ <nombre>


		# --- Comando para Leer archivo --- #
		elif re.match("leer [a-z]", self.__comandoL):
			self.__agregarComando(self.__comandoL)
			self.__copia = self.__comandoL.strip()  # -> Le quitamos los espacios a lo que escribio
			self.__leer(self.__copia[5:])  # -> Le madamos solo el nombre ~leer~ <nombre>


		# --- Comando para pasar contendio --- #
		elif re.match("psr -cont -de [a-z]", self.__comandoL):
			self.__agregarComando(self.__comandoL)

			self.__copia = self.__comandoL.split(" ") # -> Crea una lista = [psr, -cont, -de, archivo.extension]
			self.__psr(self.__copia[3])


		# --- Comando para ver los recientes --- #
		elif self.__comandoL == "viewC":
			for i in range(len(self.__comandosUsados)):
				print(self.__comandosUsados[i])
			print("\n")
			self.__inicio()


		# --- Comando para ver todos los comandos y sus acciones
		elif self.__comandoL == "ayu":
			self.__comandosUsados.append(self.__comandoL)
			print("""
			gb => Salir del explorador
			exp <nombre> => Ingresar a una carpeta
			ex <n> => Retroceder n carpetas
			lim => Limpiar la pantalla
			df => Ver los archivos y carpetas del path actual
			cr <nombre> => Crear archivo/carpeta
			br <nombre> => Borrar archivo/carpeta
			rnm <nombre> => Renombrar archivos/carpetas
			leer <nombre> => Leer contenido de un archivo
			psr -cont de <nombre> => Pasarc contenido de un archivo a otro
			viewC => Ver comandos que han sido usados recientemente
			ayu => Lo acabo de usar, ya sabe para que es
			color [1, 4] => {
				Cambiar color de la letra:
				1 = Amarillo brillante
				2 = Verde brillante
				3 = Azul brillante
				4 = Blanco
			}
			\n""")

			self.__inicio()
		

		# --- Comando para cambiar color del foreground --- #
		elif re.search("color [1-4]", self.__comandoL):
			print(self.__comandoL[6:])
			if self.__comandoL[6:] == "1":
				self.__colorFg = Fore.LIGHTYELLOW_EX

			elif self.__comandoL[6:] == "2":
				self.__colorFg = Fore.LIGHTGREEN_EX

			elif self.__comandoL[6:] == "3":
				self.__colorFg = Fore.LIGHTBLUE_EX

			elif self.__comandoL[6:] == "4":
				self.__colorFg = Fore.LIGHTWHITE_EX

			self.__inicio()


		else:
			print("Comando no conocido '{}'".format(self.__comandoL))
			print("\n")
			self.__inicio()





	# ------------------- Agregando ------------------- #
	def __agregarComando(self, comm):
		self.__comandosUsados += [comm]



	# ------------------- Comando exp ------------------- #
	def __exp(self, dir):
		if os.path.isdir(self.__path_now + "\\{}".format(dir)):

			if self.__path_now != "C:\\":
				# Este if es para estetica, ya que si esta en "C:"
				# la ruta será "C:\" entonces si entra a otra carpeta
				# quedara asi: "C:\\Carpeta" en vez de "C:\Carpeta"

				# Actualizamos el path y el contador
				self.__path_now = os.path.join(self.__path_now + "\\" + dir)
				self.__contadorDeRutas = self.__contadorDeRutas+1

				# Volvemos
				print("\n")
				self.__inicio()

			else:
				# Actualizamos el path y el contador
				self.__path_now = os.path.join(self.__path_now + dir)
				self.__contadorDeRutas = self.__contadorDeRutas + 1

				# Volvemos
				print("\n")
				self.__inicio()

		else:
			print("Carpeta '{}' no reconocida\n".format(dir))
			self.__inicio()



	# ------------------- Comando ex ------------------- #
	def __ex(self, Ndir):

		self.__lista_carpetas = self.__path_now.split('\\',) # -> Creamos una lista con la secuencia de carpetas de la ruta
		self.__str_ = "" # -> Creamos una lista donde se almacenara la nueva ruta


		# Hicimos este if por si Ndir > al numero de carpetas que lleva, es para controlar
		# el uso del comando "ex", la minima carpeta a la que puede llegar es a "C:\"
		if len(self.__lista_carpetas) >= 1 and Ndir <= len(self.__lista_carpetas)-1:

			# Resolvimos un bug que existia, que cada que se retrocedia
			# se creaba una cadena sin texto, y eso jodia el proceso
			if "" in self.__lista_carpetas:
				self.__lista_carpetas.remove("")

			# Para retroceder hicimos este sistema que lo que hace es
			# contar el numero de carpetas abiertas, lo llamaremos X
			# y a X le restamos el núemero de directorios que se quiere retroceder
			# como lo que nos quedara es una resta: X - Ndir
			# Lo restante será el numero de carpetas
			for ex in range(len(self.__lista_carpetas)-Ndir):
				self.__str_ += "{}\\".format(self.__lista_carpetas[ex])


			# Actualizamos los datos
			self.__path_now = os.path.join(self.__str_[0: len(self.__str_)-1]) # len()-1 para que no agregue el ""
			self.__contadorDeRutas = self.__contadorDeRutas+1
			print("\n")
			self.__inicio()

		else:
			# Si se exede con los directorios a los que quiere retroceder lo mandaremos a C:
			self.__path_now = os.path.join("C:\\")
			print("\n")
			self.__inicio()



	# ------------------- Comando df ------------------- #
	def __verArchivos(self):

		# Creamos una lista con los archivos que tiene el directorio actual
		self.__listaArchivos = os.listdir(self.__path_now)

		# Listas donde se guardaran las respectivas carpetas y los archivos
		self.__files = []
		self.__dir = []

		# Listas donde se guardaran solo la info de los archivos
		self.__size = []
		self.__lastAcceso = []
		self.__dateCreacion = []



		for i in range(len(self.__listaArchivos)):
			# Con este bucle pretendemos saber cuales son los archivos y cuales son carpetas
			# y los añadimos a la lista correspondiente
			if os.path.isfile(self.__path_now + "\\" + self.__listaArchivos[i]):
				self.__files.append(self.__listaArchivos[i])
			else:
				self.__dir.append(self.__listaArchivos[i])


		for info in range(len(self.__files)):
			# Con este bucle almacenaremos la informacion
			# de cada archivo
			self.__file_actual = self.__path_now + "\\" + self.__files[info]

			self.__size.append(os.path.getsize(self.__file_actual))
			self.__lastAcceso.append(time.ctime(os.path.getatime(self.__file_actual)))
			self.__dateCreacion.append(time.ctime(os.path.getmtime(self.__file_actual)))


		if self.__files:
			# Si en la carpeta de archivos hay elementos hara una tabla
			# con los propios y su información
			self.__caracteristicas = []
			for i in range(len(self.__size)):
				self.__caracteristicas.append([self.__files[i], self.__size[i], self.__lastAcceso[i], self.__dateCreacion[i]])

			print("\n",tabulate(
				self.__caracteristicas, ("Nombre", "Tamaño (Kb)", "Ultimo acceso", "Fecha de creacion"),
				tablefmt = "psql"
				)
			)
		else:
			print("No hay archivos")


		if self.__dir:
			# Funciona de igual modo que el if de arriba
			# solo que acá no hara una tabla
			print("\nCarpetas:")
			for carp in range(len(self.__dir)):
				print("   > {}".format(self.__dir[carp]))
		else:
			print("No hay carpetas")

		print("\n")
		self.__inicio()



	# ------------------- cr ------------------- #
	def __crearArchivo(self, nombre):
		self.__archivo_o_dir = input("\n   > Archivo[f] || Carpeta[d]: ").lower()

		if self.__archivo_o_dir == "d":
			# Si la carpeta existe lo crea, sino lo informa
			if os.path.isdir(self.__path_now + "\\" + nombre):
				print("La carpeta '{}' ya existe".format(nombre))
				print("\n")
				self.__inicio()

			else:
				os.mkdir(self.__path_now + "\\" + nombre)
				print("\n")
				self.__inicio()

		elif self.__archivo_o_dir == "f":

			self.__extension = input("\n   > {}.".format(nombre))
			self.__extension.strip() # -> Borra espacios
			self.__nombreCompleto = nombre + "." + self.__extension

			if os.path.isdir(self.__path_now + "\\" + self.__nombreCompleto):
				# Si el archivo existe lo crea, sino lo informa
				print("Archivo '{}' ya existe".format(self.__nombreCompleto))
				print("\n")
				self.__inicio()

			else:
				open(self.__path_now + "\\" + self.__nombreCompleto, "w")
				print("\n")
				self.__inicio()



	# ------------------- br ------------------- #
	def __borrar(self, nombre):
		self.__archivo_o_dir_ = input("\n\t> Archivo[f] || Carpeta[d]: ").lower()

		if self.__archivo_o_dir_ == "f":

			if os.path.isfile(self.__path_now + "\\" + nombre):
				os.remove(self.__path_now + "\\" + nombre)
				print("\tEliminado con exito\n")
				self.__inicio()

			else:
				print("\t'{}' no encontrado, mira si lo escribiste bien y le agregaste la extension\n".format(nombre))
				self.__inicio()


		elif self.__archivo_o_dir_ == "d":

			if os.path.isdir(self.__path_now + "\\" + nombre): # -> Vemos si existe la carpeta

				# Ahora debemos ver si dentro de esa carpeta
				# hay cosas, al menos para avisarle al usuario

				self.__archivosDentro = os.listdir(self.__path_now + "\\" + nombre) # -> Esta será la lista con la info

				if not self.__archivosDentro: # -> Si esta vacia
					os.rmdir(self.__path_now + "\\" + nombre)
					print("\tEliminada con exito\n")
					self.__inicio()

				else:
					self.__seguro = input("\n\tHay archivos en esta ruta, ¿quieres borrarlos también? [s/n]: ")
					if self.__seguro == "s":
						# Borra TODO_
						rmtree(self.__path_now + "\\" + nombre)
						print("\n\tBorrado con exito\n")
						self.__inicio()
					else:
						print("\n")
						self.__inicio()

			else:
				print("\t'{}' no encontrado, mira si lo escribiste bien\n".format(nombre))
				self.__inicio()




		else:
			print("\n\t¿{}?\n".format(self.__archivo_o_dir_))
			self.__inicio()



	# ------------------- rnm ------------------- #
	def __renombrar(self, nombre):

		# Para carpetas
		if os.path.isdir(self.__path_now + "\\" + nombre):

			self.__newName = input("\n\tNuevo nombre para la carpeta: ")
			os.renames(self.__path_now + "\\" + nombre, self.__path_now + "\\" + self.__newName)
			print("\n\tRenombrado con exito\n")
			self.__inicio()


		# Para archivos
		elif os.path.isfile(self.__path_now + "\\" + nombre):

			self.__newName = input("\n\tNuevo nombre con extension: ")
			os.renames(self.__path_now + "\\" + nombre, self.__path_now + "\\" + self.__newName)
			print("\n\tRenomnbrado con exito\n")
			self.__inicio()

		else:

			print("\n\t'{}' no encontrada\n".format(nombre))
			self.__inicio()



	# ------------------- leer ------------------- #
	def __leer(self, nombreFile):
		if os.path.isfile(self.__path_now + "\\" + nombreFile):

			self.__nuestroArch = open(self.__path_now + "\\" + nombreFile, "r", encoding = "utf-8")
			self.__listaDeLineas = self.__nuestroArch.readlines() # -> Lista con cada linea del file
			print("\n")
			for i in range(len(self.__listaDeLineas)):
				print(i+1, self.__listaDeLineas[i])

			print("\n")
			self.__inicio()


		else:
			print("{} no existente\n".format(nombreFile))
			self.__inicio()



	# ------------------- psr -content -de [a-z] ------------------- #
	def __psr(self, archivoContent):

		if os.path.isfile(self.__path_now + "\\" + archivoContent):

			# self.__archivoOriginal = Archivo donde esta el contenido
			# self.__nuevoContent = Archivo al que se le pasa e contenido
			self.__archivoOriginal = open(self.__path_now + "\\" + archivoContent, "r", encoding = "utf-8")
			self.__listaLineas = self.__archivoOriginal.readlines() # -> Lista con los renglones

			print("\n\tNumero de lineas: {}".format(len(self.__listaLineas)))

			# Pide el directorio donde esta el archivo al que se le quiere escribir el contenido
			self.__rutaDondeEsta = input("\n\tLa ruta donde esta el archivo al que se quiere pasar el contenido: ")


			# Si el directorio existe
			if os.path.isdir(self.__rutaDondeEsta):

				# Le quitamos el "\" si es que lo puso
				if self.__rutaDondeEsta.endswith("\\"):
					self.__rutaDondeEsta = self.__rutaDondeEsta[0:len(self.__rutaDondeEsta)-1]

				# Nombre del archivo
				self.__nombre_fn = input("\n\tNombre del archivo {}\: ".format(self.__rutaDondeEsta))

				# Si el archivo existe
				if os.path.isfile(self.__rutaDondeEsta + "\\" + self.__nombre_fn):

					self.__nuevoContent = open(self.__rutaDondeEsta + "\\" + self.__nombre_fn, "r+")

					# Le preguntamos si quiere que le pongamos una marca
					# desde donde empezo a escribir
					self.__marca = input("\n\tQuieres que pongamos una marca desde donde empezo a escribir (s/n): ").lower()


					self.__cursor = 0
					for i in range(len(self.__nuevoContent.read())):
						self.__cursor+=1


					# Ubicamos el cursor en la ultima linea o en el ultimo caracter del texto
					# Esto para que no sobreescriba
					self.__nuevoContent.seek(self.__cursor)

					if self.__marca == "s":
						self.__nuevoContent.write("\n\n------------- Desde acá -------------\n")

					for linea in range(len(self.__listaLineas)):
						self.__nuevoContent.writelines(self.__listaLineas[linea])



				else:
					print("EL archivo {} no existe\n".format(self.__nombre_fn))
					self.__inicio()
			else:
				print("La ruta {} no existe\n".format(self.__rutaDondeEsta))
				self.__inicio()
		else:
			print("El archivo {} no existe\n".format(archivoContent))
			self.__inicio()




if __name__ == '__main__' : init = Main(os.getcwd())
