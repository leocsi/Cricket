from OpenSSL import crypto
import os
import getpass

def generate_ca():
    key = new_key_pair(2048)
    careq = new_cert_request(key, CN="Cricket Root Certificate Authority")
    cacert = new_cert(careq, careq, key, 0, 0, 60*60*24*365*2)
    path = "light_server/security/certs"
    if not os.path.exists(path):
        os.makedirs(path)
    keyfile = open(path+"/CA.pkey","w")
    keyfile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key, cipher="aes-256-cbc", passphrase=get_passwd).decode("utf-8"))
    certfile = open(path+'/CA.cert', 'w')
    certfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cacert).decode("utf-8"))

def generate_cert(file_name, cert_name):
    key = new_key_pair(2048)
    req = new_cert_request(key, CN=cert_name)
    ca = crypto.load_certificate(crypto.FILETYPE_PEM, open("light_server/security/certs/CA.cert","rb").read())
    cakey = crypto.load_privatekey(crypto.FILETYPE_PEM, open("light_server/security/certs/CA.pkey","rb").read(),passphrase=get_passwd)
    cert = new_cert(req, ca, cakey, 0, 0, 60*60*24*365)
    open(f"light_server/security/certs/{file_name}.cert",'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    open(f"light_server/security/certs/{file_name}.pkey",'w').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key, cipher="aes-256-cbc", passphrase=get_passwd).decode("utf-8"))

def generate_crl():
    pass

def revoke_cert():
    pass

def new_key_pair(size: int):
    key_pair = crypto.PKey()
    key_pair.generate_key(crypto.TYPE_RSA, size)
    return key_pair

def new_cert_request(pkey, digest="sha512", **name):
    req = crypto.X509Req()
    subj = req.get_subject()
    for (key, value) in name.items():
        setattr(subj, key, value)

    req.set_pubkey(pkey)
    req.sign(pkey, digest)
    
    return req

def new_cert(req: crypto.X509Req, issuerCert: crypto.X509, issuerKey: crypto.PKey, serial, notBefore, notAfter, digest="sha512"):
    cert = crypto.X509()
    cert.set_serial_number(serial)
    
    cert.gmtime_adj_notBefore(notBefore)
    cert.gmtime_adj_notAfter(notAfter)
    
    cert.set_issuer(issuerCert.get_subject())
    
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    
    cert.sign(issuerKey, digest)
    return cert

def get_passwd(a):
    passwd = getpass.getpass("Enter a password to encrypt private key (Make sure to remember this!): ")
    return bytes(passwd,"utf-8")

      