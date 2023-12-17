'''Entry point to Cricket Light Server module. This file has 3 different run modes, which can be toggled via 
-certgen -client -server flags. The appropriate run mode will be launched, otherwise the program exits.'''

import sys, logging

from listener.listener import Listener
from security.security_manager import missing_certs, certgen
from simple_client import client_main

def light_server():
    '''This method starts light server if all the certificates are present otherwise exits'''

    if missing_certs():
        exit()

    listener = Listener()
    try:
        listener.listen()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Please specify the run mode for the application: -[certgen|client|server]. Exiting application.')
        sys.exit(1)
    run_mode = sys.argv[1]
    if run_mode == '-server':
        logging.basicConfig(filename='logs/server.log', level= logging.INFO, format='%(levelname)s:%(message)s')
        logging.info('Starting Cricket Light Server')
        
        light_server()
    elif run_mode == '-certgen':
        logging.basicConfig(filename='logs/certgen.log', level= logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
        logging.info('Starting Cricket Certificate Generator module')
        
        certgen()
    elif run_mode == '-client':
        logging.basicConfig(filename='logs/client.log', level= logging.INFO, format='%(levelname)s:%(message)s')
        logging.info('Starting Cricket Client')
    
        client_main()

    else:
        print(f'Could not recognize this flag: "{sys.argv[1]}". Try -[certgen|client|server] . Exiting application.')
        sys.exit(1)