import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import paramiko
import os

from adapt_file import adaptar_archivo

# Variables globales
archivo_a_copiar = None


def seleccionar_archivo(archivo_label):
    """Seleccionar archivo para copiar"""
    global archivo_a_copiar
    archivo_a_copiar = filedialog.askopenfilename(title="Seleccionar archivo")
    if archivo_a_copiar:
        archivo_label.config(text=f"Archivo seleccionado: {os.path.basename(archivo_a_copiar)}")


def copiar_archivo(ip_entry, archivo_label):
    """Función para copiar el archivo a la Raspberry Pi"""
    ip_raspberry = ip_entry.get()
    destino = "/home/SOA/Test/"  # Directorio de destino en la Raspberry Pi

    if not ip_raspberry:
        messagebox.showerror("Error", "Por favor, ingresa una dirección IP.")
        return

    if not archivo_a_copiar or not os.path.exists(archivo_a_copiar):
        messagebox.showerror("Error", "Por favor, selecciona un archivo válido.")
        return

    # Pedir usuario y contraseña
    usuario = simpledialog.askstring("Usuario", "Ingrese su nombre de usuario:", show="*")
    if not usuario:
        messagebox.showerror("Error", "El nombre de usuario es obligatorio.")
        return

    contrasena = simpledialog.askstring("Contraseña", "Ingrese su contraseña:", show="*")
    if not contrasena:
        messagebox.showerror("Error", "La contraseña es obligatoria.")
        return

    try:

        # Conexión SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_raspberry, username=usuario, password=contrasena)

        archivo_RPI=adaptar_archivo(archivo_a_copiar)

        # Copia del archivo usando SFTP
        sftp = ssh.open_sftp()
        sftp.put(archivo_RPI, f"{destino}{os.path.basename(archivo_RPI)}")
        sftp.close()
        ssh.close()

        messagebox.showinfo("Éxito", "Archivo copiado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo copiar el archivo: {e}")


def show_window(icon, item):
    """Muestra la ventana principal para copiar archivos."""
    # Crear la ventana
    root = tk.Tk()
    root.title("Copiar archivo a Raspberry Pi")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    # Dirección IP de la Raspberry Pi
    tk.Label(frame, text="Dirección IP de la Raspberry Pi:").grid(row=0, column=0, sticky="w")
    ip_entry = tk.Entry(frame, width=30)
    ip_entry.grid(row=0, column=1)

    archivo_label = tk.Label(frame, text="No se ha seleccionado ningún archivo")
    archivo_label.grid(row=1, column=0, columnspan=2, sticky="w")

    # Botón para seleccionar archivo
    seleccionar_btn = tk.Button(frame, text="Ejecutar Servidor Pigpio...", command=lambda: seleccionar_archivo(archivo_label))
    seleccionar_btn.grid(row=2, column=0, columnspan=2, pady=5)

    # Botón para seleccionar archivo
    seleccionar_btn = tk.Button(frame, text="Seleccionar archivo", command=lambda: seleccionar_archivo(archivo_label))
    seleccionar_btn.grid(row=2, column=0, columnspan=2, pady=5)

    # Botón para copiar archivo
    copiar_btn = tk.Button(frame, text="Copiar archivo", command=lambda: copiar_archivo(ip_entry, archivo_label))
    copiar_btn.grid(row=3, column=0, columnspan=2, pady=10)

    # Cuando se cierre la ventana, se destruye, pero el icono sigue visible
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    root.mainloop()
