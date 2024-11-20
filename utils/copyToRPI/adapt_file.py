from pathlib import Path
import re
import os


GPIOZERO_ORIGINAL = "simu_docker_rpi.gpiozero"
GPIOZERO_SALIDA = "gpiozero"
CIRCUIT_PLATFORM_ORIGINAL = "from simu_docker_rpi.CircuitPlatform import Circuit_Platform"
CIRCUIT_PLATFORM_SALIDA = ""

# Expresión regular para encontrar la línea que contiene 'Circuit_Platform.check_plataform_simulator'
CHECK_PLATFORM_ORIGINAL= r'.*Circuit_Platform\.check_plataform_simulator.*\n?'
CHECK_PLATFORM_SALIDA   = '\tmain()\n'

def obtener_nombre_RPI(archivo_original):

    # Separar la ruta del archivo y el nombre del archivo con su extensión
    ruta_directorio, nombre_archivo = os.path.split(archivo_original)

    # Separar el nombre del archivo de su extensión
    nombre, extension = os.path.splitext(nombre_archivo)

    # Crear el nuevo nombre agregando 'RPI' antes de la extensión
    nuevo_nombre_archivo = f"{nombre}RPI{extension}"

    # Obtener la nueva ruta completa
    nueva_ruta_completa = os.path.join(ruta_directorio, nuevo_nombre_archivo)

    print(f"Nueva ruta completa: {nueva_ruta_completa}")

    return nueva_ruta_completa
def copiar_archivo(archivo_original, archivo_copia):
    # Abrir el archivo original y el archivo de destino
    with open(archivo_original, "rb") as src_file:
        with open(archivo_copia, "wb") as dst_file:
            # Leer el contenido del archivo original y escribirlo en el archivo de destino
            dst_file.write(src_file.read())


def buscar_renombrar_texto(nombre_archivo):
    # Lee el contenido del archivo original
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    # Reemplaza el string
    contenido = contenido.replace(GPIOZERO_ORIGINAL, GPIOZERO_SALIDA)
    contenido = contenido.replace(CIRCUIT_PLATFORM_ORIGINAL, CIRCUIT_PLATFORM_SALIDA)

    contenido = re.sub(CHECK_PLATFORM_ORIGINAL,CHECK_PLATFORM_SALIDA,contenido)
    #contenido= re.sub(r'.*Circuit_Platform\.check_plataform_simulator.*\n?', '\tmain()\n', contenido)

    # Guarda el contenido modificado en el archivo de salida
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    print(f"Se adapto el archivo '{nombre_archivo}'.")


def adaptar_archivo(nombre_archivo):
    extension = Path(nombre_archivo).suffix

    if extension != ".py":
        return

    archivo_salida = obtener_nombre_RPI(nombre_archivo)

    copiar_archivo(nombre_archivo, archivo_salida)
    buscar_renombrar_texto(archivo_salida)
    return archivo_salida

