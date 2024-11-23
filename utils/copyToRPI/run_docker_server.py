import subprocess
from tkinter import messagebox

def execute_docker_server():
    # Comando de Docker
    command = [
        "docker", "run",
        "--network", "bridge",
        "-p", "22:22",
        "-p", "5000:5000",
        "-p", "5022:5022",
        "soaunlam/emulador-raspberry-pigpio"
    ]

    try:
        # Ejecutar el comando
        subprocess.run(command, check=True)
        messagebox.showinfo("Éxito", "Ejecutando server Pigpio en Docker.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        messagebox.showerror("Error", f"Error al ejecutar el comando: {e}")

    except FileNotFoundError:
        messagebox.showerror("Error", "Docker no está instalado o no se encuentra en el PATH.")
