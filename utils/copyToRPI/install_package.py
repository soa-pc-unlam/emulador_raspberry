import subprocess
import importlib.metadata
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

def is_package_installed(package_name):
    """Verifica si un paquete ya está instalado usando importlib.metadata."""
    try:
        importlib.metadata.version(package_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False


def install_package():
    package_name = "simu-docker-rpi"
    if is_package_installed(package_name):
        print(f"El paquete '{package_name}' ya está instalado.")
        messagebox.showinfo("Info", f"El paquete '{package_name}' ya está instalado.")
        return

    try:
        install_package_in_new_console()
        #messagebox.showinfo("Éxito", "Paquete instalado correctamente.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al ejecutar el comando: {e}")


def install_package_in_new_console():
    package_name = "simu-docker-rpi"
    command = (
        f'start cmd /c "pip install -i https://test.pypi.org/simple '
        f'--extra-index-url https://pypi.org/simple {package_name} & pause"'
    )
    os.system(command)
