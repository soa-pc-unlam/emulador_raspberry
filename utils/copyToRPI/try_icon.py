import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from copiar_archivo import show_window


def create_image():
    """Crea un ícono para la bandeja del sistema."""
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill=(0, 128, 255))
    return image


def quit_app(icon, item):
    """Cierra la aplicación."""
    icon.stop()


def run_tray():
    """Ejecuta el icono de la bandeja del sistema."""
    icon_image = create_image()
    menu = Menu(
        MenuItem("Mostrar", lambda icon, item: show_window(icon, item)),
        MenuItem("Salir", quit_app)
    )
    icon = Icon("Copiar a Raspberry", icon_image, menu=menu)

    icon.run()


# Inicia la interfaz de la bandeja del sistema
if __name__ == "__main__":
    # Ejecutar el tray icon en un hilo separado
    tray_thread = threading.Thread(target=run_tray, daemon=True)
    tray_thread.start()

    # Mantener el programa principal en ejecución
    tray_thread.join()  # Esto asegura que el programa no termine hasta que se cierre el icono
