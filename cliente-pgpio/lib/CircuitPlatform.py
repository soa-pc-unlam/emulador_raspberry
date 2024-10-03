from json import load

class Circuit_Platform:
    @classmethod
    def check_plataform_simulator(cls, nameFileJson, decoraterFunction):
        """
        Función que determina si se está ejecutando el script en un simulador
        o en una Raspberry Pi física.

        Args:
            nameFileJson: Nombre del archivo JSON que indica
                          los componentes gráficos que se deben usar.
            decoraterFunction: Función decoradora que se va a invocar para manejar
                               los componentes gráficos. Sería el Backend.
        """
        try:
            if cls._is_simulator():
                print("Este script está corriendo en un simulador de Raspberry Pi.")
                cls._create_circuit(nameFileJson, decoraterFunction)
            else:
                print("Este script está corriendo en una Raspberry Pi física.")
                decoraterFunction()

        except Exception as e:
            # Captura cualquier excepción y la maneja
            print(f"Ha ocurrido un error al ejecutar en la plataforma: {e}")

    @classmethod
    def _is_simulator(cls):
        try:
            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read()
                # Si es un simulador, puede que no tenga 'BCM' o 'Raspberry Pi'
                if "Raspberry Pi" not in cpuinfo and "BCM" not in cpuinfo:
                    return True
        except FileNotFoundError:
            return True
        return False

    @classmethod
    def _create_circuit(cls, nameFileJson, decoraterFunction):
        from lib.tkgpio import TkCircuit
        """
        Función que se utiliza para crear el circuito gráfico.
        Esta función crea el circuito en base al archivo JSON
        que indica los componentes del mismo.

        Args:
            nameFileJson: Nombre del archivo JSON que indica
                          los componentes gráficos que se deben usar.
            decoraterFunction: Función decoradora que se va a invocar para manejar
                               los componentes gráficos. Sería el Backend.
        """
        try:
            with open(nameFileJson, "r") as file:
                configuration = load(file)

            circuit = TkCircuit(configuration)
            # Usar el decorador @circuit.run con la función main
            circuit.run(decoraterFunction)
        except FileNotFoundError:
            print(f"El archivo {nameFileJson} no fue encontrado.")
        except Exception as e:
            print(f"Error al crear el circuito gráfico: {e}")
