import sys

from listener.listener import Listener
from security.security_manager import missing_certs, certgen
from simple_client import client_main

def light_server():
    if missing_certs():
        exit()

    listener = Listener()
    try:
        listener.listen()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run_mode = sys.argv[1]
    if run_mode == '-server':
        light_server()
    elif run_mode == '-certgen':
        certgen()
    elif run_mode == '-client':
        client_main()