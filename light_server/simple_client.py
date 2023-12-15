import socket, time
from OpenSSL import SSL, crypto

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def verify_cb(conn: SSL.Connection, cert: crypto.X509, error: int, depth: int, ret: int):
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


def client_main():
    ctx = SSL.Context(SSL.TLSv1_2_METHOD)
    ctx.set_verify(SSL.VERIFY_PEER, verify_cb) # Demand a certificate
    ctx.use_privatekey_file ("light_server/security/certs/client.pkey")
    ctx.use_certificate_file("light_server/security/certs/client.cert")
    ctx.load_verify_locations("light_server/security/certs/ca.cert")

    retry_count, retry_limit = 0, 10
    while True:
        try:
            sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            sock.connect((HOST, PORT))
            print('Connected!')
            retry_count = 0
            command = ""
            while command != "x":
                command = input('Type command: ')
                sock.sendall(bytes(command, "utf-8"))
                
        except Exception:
            if retry_count == 0:
                print('Something went wrong with the server.')
            if retry_count <= retry_limit:
                if retry_count % 2 == 0:
                    print(f"Retrying connection... ({retry_count}/{retry_limit})")
                retry_count += 1
                continue
            else:
                print("Server unavailable.")
                break

if __name__ == '__main__':
    client_main()