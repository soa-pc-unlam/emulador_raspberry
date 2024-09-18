from lib.tkgpio import TkCircuit
from json import load

def create_circuit(nameFileJson, decoraterFunction):
    """
       Funcion que se utiliza para crear el cirtcuito grafico.
       Esta funcion crea el cirucito en base al archivo json
       que indica los componentes del mismo

       Args:
           nameFileJson : Nombre del archivo Json que indica
                          los componentes graficos que se deben usar

           decoraterFunction: Funcion decoradr que se va a invocar para manejar
                              los compoenentes graficos. Seria el Backend
    """

    '''Zona donde se crea el circuito gráfico'''
    with open(nameFileJson, "r") as file:
        configuration = load(file)

    circuit = TkCircuit(configuration)

    # Usar el decorador @circuit.run con la función main
    circuit.run(decoraterFunction)
