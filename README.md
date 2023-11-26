# SOA-Emulador-Raspberry PI 


Este repositorio pertenece al proyecto denominado "Contenedores de ambientes simulados de sistemas embebidos para Internet de las Cosas" que se esta llevando a cabo en la Universidad Nacional de La Matanza. 
Aquí se encuentran almacenados los archivos necesarios para poder ejecutar la imagen docker con el emulador Qemu,que esta configurado para utilizar la placa Raspberry PI en forma virtual

El directorio Kernel posee el Kernel de la imagen del S.O Raspbian, que fue adaptado con los programas necesarios para poder funcionar.Por otro lado el archivo de la imagen de la raspberry pi  .cow se subio a google drive, debido a que github no permite subir tamaños de archivos grandes.

## Pasos de ejecucion para abrir el S.O Desktop Raspbian 
1. Crear el contenedor de la imagen Docker de la siguiente manera
   `docker run -p 6080:80 soaunlam/emulador-raspberry:v2`

1. Abrir una navegador web e ingresar la siguiente URL

    `localhost:6080`
  
  Al ingresar en esta URL se abrirá un entorno gráfico de ubuntu
1. Si por defecto no se abre automaticamente el S.O Raspbian en forma GUI, se debe ejecutar en ubuntu el script llamado

  `script_start_raspbian.sh`

que se encuentra en el directorio `/root/images` 

## Pasos de ejecucion para simular los sensores y actuadores de una Raspberry en Qemu

En sección se utilizo la biblioteca creada por Wallysalami (TKGPIO). Por lo tanto, dentro del S.O Desktop Raspbian, se debe ejecutar un programa de la siguiente manera para utilizar los sensores.

`python3.7 ~/tkgpio/docs/example simple_circuit.py`
