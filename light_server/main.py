from listener.listener import Listener
from security.security_manager import Security

def main():
    security = Security()
    if security.missing_certs():
        security.cert_generator()

    listener = Listener()
    try:
        listener.listen()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()