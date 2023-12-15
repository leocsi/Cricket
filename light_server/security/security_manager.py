from security.security_utils import *
from os import path
from OpenSSL.SSL import Connection
 
CERT_PATH = "light_server/security/certs/"
'''This is where certificates are stored'''
FILES = ['ca.cert', 'ca.pkey', "server.cert","server.pkey", "crl"]
'''List of necessary files to check for.'''

def certgen():
    actions_map = {'1': default_certs,
                    '2': generate_ca,
                    '3': generate_crl,
                    '4': create_new_cert,
                    '5': create_new_cert,
                    '6': revoke_cert}
    while True:
        action = input('''\nThis is the certificate management utility for Cricket Light Server.\nPlease select what action you\'d like to perform (1-7)\n
            1. Initialize Cricket (do this before first run!)
            2. Generate new CA
            3. Generate new CRL
            4. Generate server certificate
            5. Generate client certificate
            6. Revoke certificate
            7. Exit\nAction: ''')
        if action == '7':
            break
        elif action in actions_map:
            if action == '4':
                actions_map[action]('server')
            elif action == '5':
                actions_map[action]('client')
            else:
                actions_map[action]()
        else:
            print('Could not recognize input. Please specify a number 1-7.')
def missing_certs() -> bool:
    """This function checks if any of the necessary files are missing.
    
    :returns: A boolean indicating whether there are missing files"""
    for file in FILES:
        if not path.isfile(CERT_PATH + file):
            print("Some certificates were missing or incomplete. Please run certificate generator: main.py -certgen.")
            return True
    return False


def default_certs() -> None:
    """This method generates the required certificate files for the light server application to run. 
    """

    print('Generating CA...')
    generate_ca()
    print('CA Generated!')

    print("Generating CRL...")
    generate_crl()
    print('CRL Generated!')

    print("Generating Server Certificate...")
    create_new_cert("server", "server", "Cricket Light Server")
    print("Server certificate generated!")

    if input("Would you like to create a client certificate? (Y/N)") == "Y":
        create_new_cert('client')

def create_new_cert(type:str, filename:str=None, name:str=None):
    print(f"Generating {type.title()} Certificate...")

    if not filename:
        filename = input("New certificate file name (without extension): ")
    if not name:
        name = input("New certificate Common Name: ")
    
    generate_cert(filename, type, CN=name)

    print(f"{type.title()} certificate generated!")


def skip_or_create(file_name, create_func, args=None):
    if not args:
        args = []
    if not path.isfile(CERT_PATH + file_name):
        create_func(*args)
    else:
        print(f'{file_name} already exists. Skipping creation...')


def install_certs():
    certs = [('ca.cert', generate_ca), ('crl', generate_crl), ('server.cert', create_new_cert, ['server'])]
    for cert in certs:
        skip_or_create(*cert)


def verify_cert(conn: Connection, cert: crypto.X509, error: int, depth: int, ret: int) -> bool:
    """This method is a callback for socket connection, it performs a hardened verification process, checking for certificate revocations, and strict x509 requirements

    :param conn: connection this check is being performed on
    :param cert: certificate being checked
    :param error: error code if it happened
    :param depth: how deep the current certificate in the chain is
    :param ret: return code
    :returns: A boolean indicating whether verification was successful
    """
    try:
        store = crypto.X509Store()
        
        crl = crypto.load_crl(crypto.FILETYPE_PEM, open(f"light_server/security/certs/crl",'rb').read())
        store.add_crl(crl)
        
        if crl.get_revoked():
            if hex(cert.get_serial_number())[2:] in [str(revoked.get_serial(),"utf-8").lower() for revoked in crl.get_revoked()]:
                return False
          
        ca = crypto.load_certificate(crypto.FILETYPE_PEM, open("light_server/security/certs/ca.cert","rb").read())
        store.add_cert(ca)

        store.set_flags(crypto.X509StoreFlags.CRL_CHECK_ALL | crypto.X509StoreFlags.X509_STRICT)

        storectx = crypto.X509StoreContext(store, cert)
        storectx.verify_certificate()
        return True
    except crypto.X509StoreContextError as ce:
        print(ce)
        return False
    except Exception as e:
        print(e)
        return False
    
