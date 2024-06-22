import socket
import struct
import threading
import pigpio
from datetime import datetime

gpio_state = {}
gpio_mode = {}


def setMode(pin, value):
    gpio_mode[pin] = value

def getMode(pin):
    value = -1
    if pin in gpio_mode:
        value = gpio_mode[pin]
    return value

def setState(pin, value):
    gpio_state[pin] = value


def getState(pin):
    value = -1
    if pin in gpio_state:
        value = gpio_state[pin]
    return value
def response(cmd, p1, p2):
    req = 'unknown command'
    res = -1
    # First Connection -> Bit Read? // lastLevel
    if cmd == pigpio._PI_CMD_BR1:
        req = '_PI_CMD_BR1'
        res = 10
    # Version
    elif cmd == pigpio._PI_CMD_HWVER:
        req = '_PI_CMD_HWVER'
        res = 0x902120
        res = 0xa22082 # Raspberry PI 3 Model B Rev 1.2
    # NotifyOpenInBand  // handle
    elif cmd == pigpio._PI_CMD_NOIB:
        req = '_PI_CMD_NOIB'
        res = 99
    # Set Pin Mode
    elif cmd == pigpio._PI_CMD_MODES:
        req = '_PI_CMD_MODES'
        setMode(p1, p2)
        res = 1
        # Get Pin Mode
    elif cmd == pigpio._PI_CMD_MODEG:
        req = '_PI_CMD_MODEG'
        res = getMode(p1)
    # Sets or clears the internal GPIO pull-up/down resistor.
    elif cmd == pigpio._PI_CMD_PUD:
        req = '_PI_CMD_PUD'
        res = 1
    # Glitch Filter
    elif cmd == pigpio._PI_CMD_FG:
        req = '_PI_CMD_FG'
        res = 1
    # Write
    elif cmd == pigpio._PI_CMD_WRITE:
        req = '_PI_CMD_WRITE'
        setState(p1, p2)
        res = 1
    elif cmd == pigpio._PI_CMD_READ:
        req = '_PI_CMD_READ'
        res = getState(p1)

    print(f"request:{req}, cmd:{cmd}, p1: {p1}, p2: {p2}")
    print(f"response: {res}")
    return res

def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024)
            print(f"Message Received at {datetime.now().strftime("%H:%M:%S.%f")}")
            unpacked_values = struct.unpack('IIII', request)
            cmd, p1, p2, _ = unpacked_values

            dummy = b'Hello, World'
            client_socket.send(struct.pack('12sI', dummy, response(cmd, p1, p2)))

    except Exception as e:
        print(f"Error al manejar la conexión: {e}")

    finally:
        client_socket.close()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
serversocket.bind(('127.0.0.1', 5000))
serversocket.listen(5)

while True:

    clientsocket, address = serversocket.accept()
    print(f"Connection from {address}")

    client_handler = threading.Thread(target=handle_client, args=(clientsocket,))
    client_handler.start()
