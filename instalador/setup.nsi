Name "simu-docker-rpi"          

# Solicitar permisos de administrador
RequestExecutionLevel admin

# Incluir complementos
!include "LogicLib.nsh"
!include "MUI2.nsh"
!include x64.nsh


!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_COMPONENTS ; Página para seleccionar componentes
!insertmacro MUI_PAGE_DIRECTORY ; Página para seleccionar directorio
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "Spanish"

# Directorio y nombre de instalación predeterminado
OutFile "setup-simu-docker-rpi.exe"
InstallDir "c:\simu-docker-rpi"


# Path de archivos de instalación
!define INSTALL_DIR_ORIGIN ".\"
!define INSTALL_DIR_DOCKER_COMPOSE "\docker\"
# Definir las URL de descarga
!define DOCKER_INSTALLER_URL "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
!define PYTHON_INSTALLER_URL "https://www.python.org/ftp/python/3.11.4/python-3.11.4.exe"

# Componentes
!define COMPONENT_DOCKER "Crear imagen Docker"

var DockerPath

SectionGroup "Requisitos del sistema"
	
    Section "Instalar Docker"
		SectionIn RO #Esta seccion es obligatoria        
		Call VerificarDocker
    SectionEnd
	Section "Instalar Python y pip"
		SectionIn RO #Esta seccion es obligatoria    
		Call VerificarPython
        Call VerificarPip
    SectionEnd
	Section "Instalar configuracion"
		SectionIn RO #Esta seccion es obligatoria    
		# Crear directorio de instalación
		CreateDirectory "$INSTDIR"

		# Copiar archivos al directorio de instalación
		SetOutPath "$INSTDIR"
		File /r "${INSTALL_DIR_ORIGIN}\*.*"
	SectionEnd
	# Sección de desinstalación
	Section "Limpieza de instalacion"
		SectionIn RO #Esta seccion es obligatoria        
		# Eliminar archivos y directorios
		Delete "$INSTDIR\*.*"
		RMDir "$INSTDIR"
		Delete $TEMP\DockerInstaller.exe
		Delete $TEMP\PythonInstaller.exe

	SectionEnd
		
SectionGroupEnd


Section "Crear Contenedores Docker"
	# Esta sección es opcional para crear y contenedores las imagenes usando Docker Compose
	call EjecutarDockerDesktop
	StrCmp $0 "true" DescargarImagenDocker CancelarDescarga
	
	CancelarDescarga:
		Return
	
	DescargarImagenDocker:	
		#una vez iniciado Docker Desktop se ejecuta el archivo docker-compose
		StrCpy $0 "$INSTDIR${INSTALL_DIR_DOCKER_COMPOSE}docker-compose.yml"  ; Ruta del docker compose
		
		IfFileExists "$0" ArchivoComposeExiste ArchivoComposeNoExiste
		
		ArchivoComposeExiste:
			SetOutPath "$INSTDIR${INSTALL_DIR_DOCKER_COMPOSE}"
			ExecWait '"$SYSDIR\cmd.exe" /k echo "Instalando Docker COMPSE, por favor espere..." && docker-compose up -d && timeout /T 3 && exit'
			MessageBox MB_OK "Se ha instalado y ejecutado los contendores Docker."
			Return

		ArchivoComposeNoExiste:
			MessageBox MB_OK "No se ha instalado correctamente el archivo de Docker-Compose.yml"
			Return
		
SectionEnd


Function EjecutarDockerDesktop
    # Leer clave en HKLM
	
	${If} ${RunningX64}
		SetRegView 64
	${EndIf}

	
	ReadRegStr $DockerPath HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Docker Desktop" "InstallLocation"   
    # Verificar si la clave está vacía
    StrCmp $DockerPath "" ComprobarHKCU 0
    Goto EjecutarDocker

    ComprobarHKCU:
        # Leer clave en HKCU
        ReadRegStr $DockerPath HKCU "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Docker Desktop" "InstallLocation"
        StrCmp $DockerPath "" NoEncontrado 0
        

    EjecutarDocker:
        # Asegurarte de que el ejecutable se encuentra
        IfFileExists "$DockerPath\Docker Desktop.exe" EjecutarAhora
        MessageBox MB_OK "Error: No se encontró el ejecutable en $DockerPath\Docker Desktop.exe"
        Goto NoEncontrado

     EjecutarAhora:
	 	SetOutPath "$DockerPath"
		ExecWait '"$SYSDIR\cmd.exe" /k echo "Iniciando Docker, por favor espere 20 segundos..." && "Docker Desktop.exe" && timeout /T 20 && exit'     


        StrCpy $0 "true"
        Return

    NoEncontrado:
        MessageBox MB_YESNO "Error: No se pudo iniciar Docker Desktop automáticamente. ¿Desea iniciar Docker manualmente?" IDYES RespuestaYes IDNO RespuestaNo

        RespuestaNo:
            MessageBox MB_OK "Atención: deberá descargar la imagen Docker manualmente"
            StrCpy $0 "false"
            Return

        RespuestaYes:
            MessageBox MB_OK "Asegúrese de que Docker Desktop esté iniciado para continuar"
            StrCpy $0 "true"
            Return    
FunctionEnd


# Funciones de ejecucion
Function ValidarURL
    inetc::head /silent "${DOCKER_INSTALLER_URL}" "$TEMP\head.txt"
    Pop $0  ; Captura el estado del comando

    StrCmp $0 "OK" URLValida URLInvalida

    URLValida:
        StrCpy $0 "true"  ; Retornar true
        Return
        

    URLInvalida:
        MessageBox MB_YESNO "La URL no es valida o no hay conexion a Internet.¿Desea continuar la instalacion?" IDYES Continuar IDNO Cancelar

        Cancelar:
            Quit  ; Cierra completamente el instalador

        Continuar:
			StrCpy $0 "true"  ; Retornar true
            Return
FunctionEnd

# Función para verificar si Docker está instalado
Function VerificarDocker
    nsExec::ExecToStack 'docker --version'
    Pop $0  ; Estado del comando
    Pop $1  ; Salida del comando

    StrCmp $0 "0" DockerInstalado NoDocker
	
	#NoDocker:
    DockerInstalado:
       Return
	
	#DockerInstalado:
    NoDocker:
        MessageBox MB_YESNO "Docker no esta instalado ¿Desea intentar descargar e instalar Docker automaticamente?" IDYES DescargarDocker IDNO Cancelar

        Cancelar:
            MessageBox MB_OK "La instalación ha sido cancelada."
            Quit

        DescargarDocker:
            Call DescargarDocker
            Return
FunctionEnd

# Función para descargar e instalar Docker
Function DescargarDocker
    

    Call ValidarURL
    StrCmp $0 "true" Descargar ContinuarSinDocker1


    ContinuarSinDocker1:
        Return

    Descargar:
		StrCpy $0 "$TEMP\DockerInstaller.exe"  ; Ruta para guardar el instalador temporalmente
        
		MessageBox MB_OK "Descargando Docker. Esto puede tardar unos minutos..."
        inetc::get /POPUP "" /CAPTION "Descargando Docker" "${DOCKER_INSTALLER_URL}" $0
        Pop $1 ; Obtener el estado de la descarga

        IfFileExists "$0" DescargarExito DescargarFallo

        DescargarExito:
			ExecWait '"$SYSDIR\cmd.exe" /k echo "Instalando Docker, por favor espere..." && $TEMP\DockerInstaller.exe && timeout /T 3 && exit'     
            Return

        DescargarFallo:
            MessageBox MB_YESNO "Error al descargar Docker ¿Desea continuar la instalacion sin Docker?" IDYES ContinuarSinDocker2 IDNO Cancelar

            Cancelar:
                MessageBox MB_OK "La instalacion ha sido cancelada."
                Quit

            ContinuarSinDocker2:
                Return
FunctionEnd


# Función para verificar si Python está instalado
Function VerificarPython
    nsExec::ExecToStack 'python --version'
    Pop $0  ; Estado del comando
    Pop $1  ; Salida del comando

    StrCmp $0 "0" PythonInstalado NoPython
	
	#NoPython:
    PythonInstalado:
        #MessageBox MB_OK "Python ya está instalado en este sistema."
       # Call VerificarPip
        Return
	
	#PythonInstalado:
    NoPython:
        MessageBox MB_YESNO "Python no está instalado. ¿Desea instalarlo automáticamente?" IDYES DescargarPython IDNO Cancelar

        Cancelar:
            MessageBox MB_OK "La instalación ha sido cancelada."
            Quit

        DescargarPython:
            Call DescargarPython
		#	Call VerificarPip
			
            Return
FunctionEnd

# Función para verificar si pip está instalado
Function VerificarPip
    nsExec::ExecToStack 'pip --version'
    Pop $0  ; Estado del comando
    Pop $1  ; Salida del comando

    StrCmp $0 "0" PipInstalado NoPip
	
	#NoPip:
    PipInstalado:
        Call InstalarPaquetesPip
        Return
	
	#PipInstalado:
    NoPip:
        MessageBox MB_YESNO "pip no está instalado. ¿Desea instalarlo automáticamente?" IDYES DescargarPip IDNO Cancelar

        Cancelar:
            MessageBox MB_OK "La instalación ha sido cancelada."
            Quit

        DescargarPip:
            Call DescargarPip
			Call InstalarPaquetesPip
            Return
FunctionEnd

# Función para descargar e instalar Python
Function DescargarPython
    Call ValidarURL
    StrCmp $0 "true" Descargar ContinuarSinPython1

    ContinuarSinPython1:
        Return

    Descargar:
		StrCpy $0 "$TEMP\PythonInstaller.exe"  ; Ruta para guardar el instalador temporalmente
        
		MessageBox MB_OK "Descargando Python. Esto puede tardar unos minutos..."
        inetc::get /POPUP "" /CAPTION "Descargando Python" "${PYTHON_INSTALLER_URL}" $0
        Pop $1 ; Obtener el estado de la descarga

        IfFileExists "$0" DescargarExito DescargarFallo

        DescargarExito:
            ExecWait '"$SYSDIR\cmd.exe" /c echo "Instalando Python, por favor espere..." && "$TEMP\PythonInstaller.exe" && echo "Instalación completada." && timeout /T 3 && exit'
            Return

        DescargarFallo:
            MessageBox MB_YESNO "Error al descargar Python. ¿Desea continuar la instalación sin Python?" IDYES ContinuarSinPython2 IDNO Cancelar

            Cancelar:
                MessageBox MB_OK "La instalación ha sido cancelada."
                Quit

            ContinuarSinPython2:
                Return
FunctionEnd

# Función para descargar e instalar pip
Function DescargarPip
	ExecWait '"$SYSDIR\cmd.exe" /k echo "Instalando Pip, por favor espere..." && python -m ensurepip --upgrade && echo "Instalación completada." && timeout /T 3 && exit'
    Return
FunctionEnd

Function InstalarPaquetesPip
	ExecWait '"$SYSDIR\cmd.exe" /k echo "Instalando Paquetes simu-docker-rpi, por favor espere..." && pip install -i https://test.pypi.org/simple --extra-index-url https://pypi.org/simple simu-docker-rpi && timeout /T 3 && exit'
	Return
FunctionEnd


