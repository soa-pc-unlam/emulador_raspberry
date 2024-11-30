import logging

from simu_docker_rpi import check_plataform_simulator

logging.basicConfig(level=logging.INFO)

def main(): 
    logging.info(check_plataform_simulator("ButtonOnly.json", None))


if __name__ == '__main__':
    logging.debug('>>> Estamos comenzando la ejecución del paquete.')

    main()

    logging.debug('>>> Estamos finalizando la ejecución del paquete.')