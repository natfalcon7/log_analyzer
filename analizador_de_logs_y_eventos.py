#tengo el archivo en la misma carpeta que este script
#por tanto uso una ruta relativa

#esta función carga el archivo pero linea por linea con un generador para ahorrar memoria.
#abro e itero el archivo dentro de un try/except para capturar un posible error
import re 

ruta_log = "./logs.txt"

#logs_trash = []
errores =[]
#------------abre, lee y elimina espacios linea a linea, captura error --------------------------------------------------------------------------
def cargar_logs():
	try:
		with open(ruta_log,"r") as archivo:
			for log in archivo:
				yield log.strip()

	except Exception as e:
		errores.append(f"Error: {e}")


#-----------confirma si hay elementos en cada linea, captura error-------------------------------------------------------------------------------------------------
 

def lineas_vacías(linea):
	try:
		if len(linea) > 0:
			return linea 
	except Exception as e:
		errores.append(f"Linea vacía: {e}")
	return None	


#------------confirma si la linea es separable en tres partes/chequea estructura de timestamp, usario y evento---------------------------------------------

def estructura_tres_partes(linea):
	partes = linea.split("|")
	
	patron_time = r"^\d{4}[-/.]\d{2}[-/.]\d{2}[ T]\d{2}:\d{2}:\d{2}$"
	#patron_user = r"[a-zA-Z0-9_-]+"
	
	if len(partes) != 3:
		errores.append(f"Partes inválidas")
		return None
	
	time, user, message = partes
	
	if not re.fullmatch(patron_time,time.strip()):
		errores.append(f"Timestamp inválido: {time}")

		return None

	return time.strip(), user.strip(), message.strip()	
		
#-----------------------flujo--------------------------------------------------------------

logs_for_analyze =[]

if __name__ == '__main__':
	
	for linea in cargar_logs():

		linea_limpia = lineas_vacías(linea)
		if not linea_limpia:
			continue

		resultado = estructura_tres_partes(linea_limpia)
		if resultado:
			logs_for_analyze.append(resultado)


# prueba visual
print(f"Líneas válidas: {len(logs_for_analyze)}")
print(f"Errores detectados: {len(errores)}")
