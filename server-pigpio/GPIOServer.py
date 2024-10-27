import socket
import errno
import struct
import threading
import time
import traceback


import pigpio
from datetime import datetime

MSGLEN= 16

number_pack=0

gpio_state = {}
gpio_mode = {}
gpio_Notify = {}
gpio_pwm_frequency = {}
gpio_pwm_range = {}
gpio_pwm = {}
gpio_pwm_duty_cycle = {}

result_ok = 1
result_nook = -1

request_sockets = {}
event_sockets = {}
def log(message, address):
    print(f"({address}) -  {message}")

def bucle_temporizador():
    while True:
        time.sleep(0.01)
        for pin, notify in gpio_Notify.items():
            if notify:
                setNotify(pin, False)
                seq = 1
                flags = 0
                tick = int(time.perf_counter()*1000)
                level = 0

                for pin_state,state in gpio_state.items():
                    if state:
                        level += 2 ** pin_state

                for socket in event_sockets.values():
                    socket.send(struct.pack('HHII', seq, flags, tick, level))



# Crear un hilo para el bucle del temporizador
temporizador_thread = threading.Thread(target=bucle_temporizador)
temporizador_thread.start()


def setPWMDutyCycle(pin, value):
    gpio_pwm_duty_cycle[pin] = value

def getPWMDutyCycle(pin):
    value = -1
    if pin in gpio_pwm_duty_cycle:
        value = gpio_pwm_duty_cycle[pin]
    else:
        gpio_pwm_duty_cycle[pin] = 1000
        value = gpio_pwm_duty_cycle[pin]
    return value


def setPWMRange(pin, value):
    gpio_pwm_range[pin] = value

def getPWMRange(pin):
    value = -1
    if pin in gpio_pwm_range:
        value = gpio_pwm_range[pin]
    else:
        gpio_pwm_range[pin] = 1
        value = gpio_pwm_range[pin]
    return value

def setPWMFrequency(pin, value):
    gpio_pwm_frequency[pin] = value

def getPWMFrequency(pin):
    value = -1
    if pin in gpio_pwm_frequency:
        value = gpio_pwm_frequency[pin]
    else:
        gpio_pwm_frequency[pin] = 0
        value = gpio_pwm_frequency[pin]
    return value

def setNotify(pin, value):
    gpio_Notify[pin] = value

def getNotify(pin):
    value = -1
    if pin in gpio_Notify:
        value = gpio_Notify[pin]
    else:
        gpio_Notify[pin] = 0
        value = gpio_Notify[pin]
    return value

def setMode(pin, value):
    gpio_mode[pin] = value

def getMode(pin):
    value = -1
    if pin in gpio_mode:
        value = gpio_mode[pin]
    else:
        gpio_mode[pin] = 0
        value = gpio_mode[pin]
    return value

def setState(pin, value):
    gpio_state[pin] = value


def getState(pin):
    value = -1
    if pin in gpio_state:
        value = gpio_state[pin]
    else:
        gpio_state[pin] = 0
        value = gpio_state[pin]
    return value

def response(address, cmd, p1, p2):
    req = 'unknown command'
    res = result_nook
    # First Connection -> Bit Read? // lastLevel
    if cmd == pigpio._PI_CMD_BR1:
        req = '_PI_CMD_BR1'
        res = 10
        res = 0
    # Version
    elif cmd == pigpio._PI_CMD_HWVER:
        req = '_PI_CMD_HWVER'
        res = 0x902120
        res = 0xa22082 # Raspberry PI 3 Model B Rev 1.2
    # NotifyOpenInBand  // handle
    elif cmd == pigpio._PI_CMD_NOIB:
        req = '_PI_CMD_NOIB'
        res = len(gpio_Notify)
    # Set Pin Mode
    elif cmd == pigpio._PI_CMD_MODES:
        req = '_PI_CMD_MODES'
        setMode(p1, p2)
        res = result_ok
        # Get Pin Mode
    elif cmd == pigpio._PI_CMD_MODEG:
        req = '_PI_CMD_MODEG'
        res = getMode(p1)
    # Sets or clears the internal GPIO pull-up/down resistor.
    elif cmd == pigpio._PI_CMD_PUD:
        req = '_PI_CMD_PUD'
        res = result_ok
    # Glitch Filter
    elif cmd == pigpio._PI_CMD_FG:
        req = '_PI_CMD_FG'
        res = result_ok
    # Write
    elif cmd == pigpio._PI_CMD_WRITE:
        req = '_PI_CMD_WRITE'
        setState(p1, p2)
        setNotify(p1, 1)
        res = result_ok
    # Read
    elif cmd == pigpio._PI_CMD_READ:
        req = '_PI_CMD_READ'
        res = getState(p1)
    # Notify Begin
    elif cmd == pigpio._PI_CMD_NB:
        req = '_PI_CMD_NB'
        
        setNotify(p2,p1)
        res = result_ok
    # Notify Close
    elif cmd == pigpio._PI_CMD_NC:
        req = '_PI_CMD_NC'
        
        if p2 in gpio_Notify:
            del gpio_Notify[p2]
        res = result_ok
    # Get Ticks
    elif cmd == pigpio._PI_CMD_TICK:
        req = '_PI_CMD_TICK'
        val = time.perf_counter()
        res = int(time.perf_counter()*1000)
    # Set PWM Frequency
    elif cmd == pigpio._PI_CMD_PFS:
        req = '_PI_CMD_PFS'
        setPWMFrequency(p1, p2)
        res = result_ok
    elif cmd == pigpio._PI_CMD_PFG:
        req = '_PI_CMD_PFG'
        res = getPWMFrequency(p1)
    # Set PWM Range
    elif cmd == pigpio._PI_CMD_PRS:
        req = '_PI_CMD_PRS'
        setPWMRange(p1, p2)
        res = result_ok
    
    # Get PWM Range
    elif cmd == pigpio._PI_CMD_PRG:
        req = '_PI_CMD_PRG'
        res = getPWMRange(p1)
    # Set PWM Duty Cycle
    elif cmd == pigpio._PI_CMD_PWM:
        req = '_PI_CMD_PWM'
    
        setPWMDutyCycle(p1, p2)
        res = result_ok
    # Get PWM Duty Cycle
    elif cmd == pigpio._PI_CMD_GDC:
        req = '_PI_CMD_GDC'
        res = getPWMDutyCycle(p1)

    log(f"request:{req}, cmd:{cmd}, p1: {p1}, p2: {p2}", address)
    log(f"response: {res}", address)
    return res



def handle_client(address, client_socket):
    global number_pack
    try:
        while True:
            request = client_socket.recv(1024)

            if not request:

                log("Component connection closed.", address)
                break
            
            print("\n**recibe:"+str(request))
            unpacked_values = struct.unpack('IIII', request)
            cmd, p1, p2, _ = unpacked_values

            number_pack=number_pack+1
            dummy=str(number_pack+1)
            dummy = dummy.encode('utf-8')

            print("antees de pack")
            pack_data=struct.pack('12sI', dummy, response(address,cmd, p1, p2))
            print("despues de pack")
            print("antes desend")
            print("envia;"+str(pack_data))
            client_socket.send(pack_data)
            print("despues de send")
    except socket.error as e1:
        if e1.errno == errno.WSAECONNRESET:
            log("Client connection closed.", address)
            log("Raspberry Pi Server Listening...", address)


    except Exception as e2:

        log(f"General Exception: {e2}", address)
        tb = traceback.extract_tb(e2.__traceback__)
        linea_error = tb[-1].lineno
        print(f"El error ocurrió en la línea: {linea_error}")

    finally:
        if address in request_sockets:
            del request_sockets[address]
        if address in event_sockets:
            del event_sockets[address]
        client_socket.close()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
serversocket.bind(('0.0.0.0', 5000))
serversocket.listen(5)

while True:
    log(f"Raspberry Pi Server Listening...", "")

    requestSocket, address = serversocket.accept()
    request_sockets[address[1]] = requestSocket
    request_handler1 = threading.Thread(target=handle_client, args=(address[1], requestSocket,))
    log(f"Request Socket: {address[1]}. ", address[1])

    eventSocket, address = serversocket.accept()
    event_sockets[address[1]] = eventSocket
    request_handler2 = threading.Thread(target=handle_client, args=(address[1], eventSocket,))
    log(f"Event Socket: {address[1]}. ",address[1])

    request_handler1.start()
    request_handler2.start()
