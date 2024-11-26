OutFile "setup-simu-docker-rpi.exe"
InstallDir "c:\simu-docker-rpi"

# Solicitar permisos de administrador
RequestExecutionLevel admin

# Incluir complementos
!include "LogicLib.nsh"
!include "MUI2.nsh"
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

# Path de archivos de instalación
!define INSTALL_DIR_ORIGIN "C:\instalador"
!define DOCKER_INSTALLER_URL "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"

# Sección principal de instalación
Section "Instalar"

    # Verificar si Docker está instalado
    Call VerificarDocker

    # Crear directorio de instalación
    CreateDirectory "$INSTDIR"

    # Copiar archivos al directorio de instalación
    SetOutPath "$INSTDIR"
    File /r "${INSTALL_DIR_ORIGIN}\*.*"

SectionEnd

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
	
	NoDocker:
    #DockerInstalado:
        MessageBox MB_OK "Docker ya esta instalado en este sistema."
        Return
	
	DockerInstalado:
    #NoDocker:
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
            MessageBox MB_OK "Instalando Docker.."
            ExecWait '"$SYSDIR\cmd.exe" /c "$TEMP\DockerInstaller.exe" && pause'
            MessageBox MB_OK "Docker se instalo correctamente."
            Return

        DescargarFallo:
            MessageBox MB_YESNO "Error al descargar Docker ¿Desea continuar la instalacion sin Docker?" IDYES ContinuarSinDocker2 IDNO Cancelar

            Cancelar:
                MessageBox MB_OK "La instalacion ha sido cancelada."
                Quit

            ContinuarSinDocker2:
                Return
FunctionEnd

# Sección de desinstalación
Section "Desinstalar"

    # Eliminar archivos y directorios
    Delete "$INSTDIR\*.*"
    RMDir "$INSTDIR"

    # Eliminar acceso directo
    Delete "$SMPROGRAMS\MyApp\MyApp.lnk"

SectionEnd
