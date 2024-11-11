import socket
import errno
import struct
import threading
import time
import pigpio
from datetime import datetime

gpio_state = {}
gpio_mode = {}
gpio_Notify = {}
gpio_pwm_frequency = {}
gpio_pwm_range = {}
gpio_pwm = {}
gpio_pwm_duty_cycle = {}

result_ok = 1
result_nook = -1

event_sockets = {}

finished_server=False

#locks para evitar condiciones de carrera
data_commands_locks = threading.Lock()              # Para todo los comandos 
request_sockets_lock = threading.Lock()             # Para request_sockets
events_sockets_lock = threading.Lock()              # Para events_sockets
finished_server_lock = threading.Lock()             # Para saber el estado del socket de eventos

def getFinshed_server():
    global finished_server

    with finished_server_lock:
        finish=finished_server
    return finish

def setFinished_server(value):
    global finished_server

    with finished_server_lock:
        finished_server=value

def getEventSocketsValues():

    with events_sockets_lock:
        values=event_sockets.values()
    return values

def setEventSocketsValues(socket,address):
    with events_sockets_lock:
        event_sockets[address]=socket


def log(message, address):
    print(f"({address}) -  {message}")

def bucle_temporizador():
    finish=False

    while not finish:
        time.sleep(0.01)

        #aplico un lock para evitar problemas de concurrencia en los comandos
        with data_commands_locks:
            gpio_Notify_items= getGpioNotifyItems()

        for pin, notify in gpio_Notify_items:
            if notify:
                setNotify(pin, False)
                seq = 1
                flags = 0
                tick = int(time.perf_counter()*1000)
                level = 0

                #aplico un lock para evitar problemas de concurrencia en los comandos
                with data_commands_locks:
                    setNotify(pin, False)
                    gpio_state_items=getGpioStateItems()

                for pin_state,state in gpio_state_items:
                    if state:
                        level += 2 ** pin_state

                for socket in getEventSocketsValues():
                    socket.send(struct.pack('HHII', seq, flags, tick, level))

        finish=getFinshed_server()

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

def getGpioNotifyItems():
    return list(gpio_Notify.items())

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

def getGpioStateItems():
    return list(gpio_state.items())

def determine_response(client_socket, address, cmd, p1, p2):
    req = 'unknown command'
    res = result_nook
    # First Connection -> Bit Read? // lastLevel
    if cmd == pigpio._PI_CMD_BR1:
        req = '_PI_CMD_BR1'
        res = 10
        res = 0
        setEventSocketsValues(client_socket,address)
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

def response(client_socket,address, cmd, p1, p2):

    with data_commands_locks:
        res=determine_response(client_socket,address, cmd, p1, p2)
    return res


def handle_client(address, client_socket):
    finish=False
    try:
        while not finish:
            request = client_socket.recv(1024)

            if not request:

                log("Component connection closed.", address)
                break

            unpacked_values = struct.unpack('IIII', request)
            cmd, p1, p2, _ = unpacked_values

            dummy = b'Hello, World'

            client_socket.send(struct.pack('12sI', dummy, response(client_socket,address,cmd, p1, p2)))
            
        finish=getFinshed_server()

    except socket.error as e1:
        if e1.errno == errno.WSAECONNRESET:
            log("Client connection closed.", address)

    except Exception as e2:
        log(f"General Excep tion: {e2}", address)

    finally:
        with events_sockets_lock:
            if address in event_sockets:
                del event_sockets[address]
        client_socket.close()

def main():
    handlerThread1 = None
    handlerThread2 = None
    
    try:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        serversocket.bind(('0.0.0.0', 5000))
        serversocket.listen(5)

        # Crear un hilo para el bucle del temporizador
        temporizador_thread = threading.Thread(target=bucle_temporizador)
        temporizador_thread.start()

        while True:
            time.sleep(0.01)
            print("\nRaspberry Pi Server Listening...")

            # addressInfo[0] -> IP Address
            # addressInfo[1] -> Port Address

            client_socket1, addressInfo1 = serversocket.accept()
            handlerThread1 = threading.Thread(target=handle_client, args=(addressInfo1[1], client_socket1,))
            log(f"New Socket: {addressInfo1[1]}. ", addressInfo1[1])
            time.sleep(0.01)

            client_socket2, addressInfo2 = serversocket.accept()
            handlerThread2 = threading.Thread(target=handle_client, args=(addressInfo2[1], client_socket2,))
            log(f"New Socket: {addressInfo2[1]}. ", addressInfo2[1])
            time.sleep(0.01)

            handlerThread1.start()
            handlerThread2.start()

            handlerThread1.join()
            handlerThread2.join()
    except KeyboardInterrupt:
        print("\nProgram stopped by user with Ctrl+C")
    finally:
        setFinished_server(True)

        # Verificar si los threads existen y están vivos antes de unirlos
        if handlerThread1 and handlerThread1.is_alive():
            handlerThread1.join()
        if handlerThread2 and handlerThread2.is_alive():
            handlerThread2.join()
        
        temporizador_thread.join()

        serversocket.close()
        print("Server terminated successfully...")


if __name__ == "__main__":
    main()