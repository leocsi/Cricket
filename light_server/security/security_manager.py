from security.security_utils import *
from os import path
from OpenSSL.SSL import Connection
 
CERT_PATH = "light_server/security/certs/"
FILES = ["server.cert","server.pkey","client.pkey","client.cert", "crl"]

class Security:
    """Class responsible for ensuring necessary certificates are present.
    Assumes the existence of a local CA authority."""
    def missing_certs(self) -> bool:
        """This function checks if any of the necessary files are missing.
        
        :returns: A boolean indicating whether there are missing files"""
        for file in FILES:
            if not path.isfile(CERT_PATH + file):
                print("Some certificates were missing or incomplete.")
                return True
        return False
   
    def cert_generator(self) -> None:
        """This method generates the required certificate files for the application to run. 
        """

        print("Generating CRL...")
        generate_crl()

        generate_cert("server",CN="Server Certificate")
        print("Server certificate generated!")

        if input("Would you like to create a client certificate? (Y/N)") == "Y":
            certname = input("New certificate Common Name: ")
            certfile = input("New certificate file name: ")
            self.new_client(certfile, certname)

    def new_client(self, filename:str, name:str) -> None:
        """Wrapper method to generate a new client certificate.
        
        :param filename: name of the file to place the new certificate in
        :param name: Common Name of the new certificate
        """

        generate_cert(filename, CN=name)
        print("Client certificate generated!")

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
    
