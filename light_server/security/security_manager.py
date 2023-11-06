from security.security_utils import *
from os import path
 
CERT_PATH = "light_server/security/certs/"
FILES = ["CA.cert","CA.pkey","server.cert","server.pkey","client.pkey","client.cert"]

class Security:
    def missing_certs(self):
        for file in FILES:
            if not path.isfile(CERT_PATH + file):
                print("Some certificates were missing or incomplete.")
                return True
        return False
            
    def cert_generator(self):
        print("Generating certificates...")
        generate_ca()
        print("Root CA generated.")

        generate_cert("server","Server Certificate")
        print("Server certificate generated")

        generate_cert("client","Client Certificate")
        print("Client certificate generated")


def verify_cert(a,b,c,d,e):
    return True