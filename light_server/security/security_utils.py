"""Module that supplies security related features, mainly 
related to TLS encryption. Methods assume the existence of a local CA."""


from OpenSSL import crypto
import getpass,random,os
from datetime import datetime

CERT_PATH = "light_server/security/certs/"
"""Directory where certificates for the server are stored"""

def generate_cert(file_name: str, cert_type: str, **subject: "dict[str:str]") -> None:
    """Generates a new certificate according to given attributes, assumes the existence of a local CA

    :param file_name: name of the file to dump the new certificate to 
    :param cert_type: type of certificate to generate (client, server, ca)
    :param subject: subject fields of the new certificate as key-value pairs, key has to be a valid ``X509Name`` field, such as `C` or `countryName`   
    """
    key = new_private_key(2048)

    cakey = crypto.load_privatekey(crypto.FILETYPE_PEM, open(f"{CERT_PATH}ca.pkey","rb").read(),passphrase=get_passwd)
    ca = crypto.load_certificate(crypto.FILETYPE_PEM, open(f"{CERT_PATH}ca.cert","rb").read())
    ca_subject = ca.get_subject().get_components()
    cert_subject = {str(attr,"utf-8"):str(value,"utf-8") for (attr,value) in ca_subject}
    for (attr,value) in subject.items():
        cert_subject.update({attr : value})

    req = new_cert_request(key, **cert_subject)
    cert = new_cert(req, ca, cakey, random.randint(1, 50000), 0, 60*60*24*365, 'sha512', cert_type)
    
    open(f"{CERT_PATH}{file_name}.cert",'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    open(f"{CERT_PATH}{file_name}.pkey",'w').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key, cipher="aes-256-cbc", passphrase=set_passwd).decode("utf-8"))


def generate_crl() -> None:
    """Generates a certificate revocation list, with a list of given certificates.

    :param certs: list of certificates to add to the list initally, can be None for empty crl
    """
    crl = crypto.CRL()
    crl.set_lastUpdate(bytes(get_asn1(), "utf-8"))

    ca = crypto.load_certificate(crypto.FILETYPE_PEM, open(f"{CERT_PATH}ca.cert","rb").read())
    cakey = crypto.load_privatekey(crypto.FILETYPE_PEM, open(f"{CERT_PATH}ca.pkey","rb").read(),passphrase=get_passwd)

    crl.sign(ca, cakey, b"sha512")
    open(f"{CERT_PATH}crl",'w').write(crypto.dump_crl(crypto.FILETYPE_PEM,crl).decode("utf-8"))


def revoke_cert(cert:crypto.X509, reason: bytes = b"unspecified") -> None:
    """Revokes a certificate, adding it to the CRL.

    :param cert: certificate to revoke
    :param reason: reason of revocation
    """

    crl = crypto.load_crl(crypto.FILETYPE_PEM, open(f"{CERT_PATH}crl",'rb').read())
    ca = crypto.load_certificate(crypto.FILETYPE_PEM, open(f"{CERT_PATH}ca.cert","rb").read())
    cakey = crypto.load_privatekey(crypto.FILETYPE_PEM, open(f"{CERT_PATH}ca.pkey","rb").read(),passphrase=get_passwd)

    revoked = crypto.Revoked()
    revoked.set_reason(reason)
    serial_hex = bytes(hex(cert.get_serial_number()),"ascii")[2:]
    revoked.set_serial(serial_hex)
    revoked.set_rev_date(bytes(get_asn1(), "utf-8"))
    
    crl.add_revoked(revoked)
    crl.set_lastUpdate(bytes(get_asn1(), "utf-8"))

    crl.sign(ca,cakey,b"sha512")

    open(f"{CERT_PATH}crl",'w').write(crypto.dump_crl(crypto.FILETYPE_PEM, crl).decode("utf-8"))    


def new_private_key(size: int=2048) -> crypto.PKey:
    """Generate new RSA private key

    :param size: size of new key in bits (at least 2048)
    :returns: The generated key
    """
    if size < 2048:
        print("Key too weak! Please specify at least 2048 bits for key size.")
        return None
    
    key_pair = crypto.PKey()
    key_pair.generate_key(crypto.TYPE_RSA, size)
    return key_pair


def new_cert_request(pkey: crypto.PKey, digest: str="sha512", **subject:"dict[str:str]") -> crypto.X509Name:
    """Generates a new certificate according to given attributes, assumes the existence of a local CA

    :param pkey: the key to associate with the request 
    :param digest: the hashing algorithm to be used for signing. defaults to sha512
    :param subject: subject fields of the new certificate as key-value pairs, key has to be a valid ``X509Name`` field, such as `C` or `countryName`   
    """
    req = crypto.X509Req()
    subj = req.get_subject()
    for (key, value) in subject.items():
        setattr(subj, key, value)
    req.set_pubkey(pkey)
    req.sign(pkey, digest)
    return req


def new_cert(req: crypto.X509Req, issuerCert: crypto.X509, issuerKey: crypto.PKey, serial: int, notBefore: int, notAfter: int, digest: str="sha512", cert_type: str='client'):
    """Generate new X509v3 certificate.

    :param req: Certificate request to use
    :param issuerCert: CA issuer that should sign the request
    :param issuerKey: Private key of CA
    :param serial: Serial number of new cert
    :param notBefore: Start of validity date for certificate (In seconds, starting from current time)
    :param notAfter: End of validity date for certificate (In seconds, starting from current time)
    :param digest: the hashing algorithm to be used for signing. defaults to sha512
    :param cert_type: type of the requested certificate (client, server, ca)

    :returns: ``X509`` certificate object
    """
    cert = crypto.X509()
    cert.set_serial_number(serial)
    cert.set_version(2)
    
    cert.gmtime_adj_notBefore(notBefore)
    cert.gmtime_adj_notAfter(notAfter)
    
    cert.set_issuer(issuerCert.get_subject())
    
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())

    extensions = get_extenion_suites(cert, issuerCert, cert_type)
    for suite in extensions:
        cert.add_extensions(suite)

    cert.sign(issuerKey, digest)
    return cert


def set_passwd(x) -> bytes:
    """Callback function to set password for newly generated private keys.

    :returns: inputted password in bytes format
    """
    while True:
        passwd = getpass.getpass("Enter a password to encrypt private key (Make sure to remember this!): ")
        passwd_confirm = getpass.getpass("Confirm password: ")
        if passwd == passwd_confirm:
            break
        else:
            print("Passwords do not match!")

    return bytes(passwd,"utf-8")


def get_passwd(x) -> bytes:
    """Callback function to get password to unlock a private key.

    :returns: inputted password in bytes format
    """

    passwd = getpass.getpass("Enter password for private key: ")
    return bytes(passwd,"utf-8")


def get_asn1(time: datetime=datetime.now().utcnow()) -> str:
    """ Utility function to convert given time to ASN1 format: YYYYMMDDHHMMSSZ
    
    :param time: Given timestamp to parse
    :returns: ASN1 formatted time
    """
    time = f"{time.year}{time.month:02d}{time.day:02d}{time.hour:02d}{time.minute:02d}{time.second:02d}Z"
    return time

def get_extenion_suites(subject: crypto.X509, issuer: crypto.X509, cert_type: str) -> 'list[list[crypto.X509Extension]]':
    '''Determine the required extensions depending on the type of certificate requested
    One suite of extensions means the extensions CAN be added at the same time, multiple suites SHOULD be added separately.
    The required order of adding the extensions is taken into account, hence the returned list is organised in priority order.
    
    :param subject: certificate being created
    :param issuer: issuer of the certificate
    :param cert_type: type of the requested certificate (client, server, ca)
    :returns: A list of suites(lists) containing ``X509Extension`` objects'''

    extension_suites = [[]]
    if cert_type == 'client':
        extension_suites[0].append(crypto.X509Extension(b'basicConstraints', False, b'CA:false'))
        extension_suites[0].append(crypto.X509Extension(b'nsCertType', False, b'client, email'))
        extension_suites[0].append(crypto.X509Extension(b'nsComment', False, b'OpenSSL generated Client Certificate'))
        extension_suites[0].append(crypto.X509Extension(b'subjectKeyIdentifier', False, b"hash", subject=subject))
        extension_suites[0].append(crypto.X509Extension(b'authorityKeyIdentifier', False, b"keyid:always,issuer:always",issuer=issuer))
        extension_suites[0].append(crypto.X509Extension(b'keyUsage', True, b"digitalSignature,nonRepudiation,keyEncipherment"))
        extension_suites[0].append(crypto.X509Extension(b'extendedKeyUsage',False, b"clientAuth, emailProtection"))
    elif cert_type == 'server':
        extension_suites[0].append(crypto.X509Extension(b'basicConstraints', False, b'CA:false'))
        extension_suites[0].append(crypto.X509Extension(b'nsCertType', False, b'server'))
        extension_suites[0].append(crypto.X509Extension(b'nsComment', False, b'OpenSSL generated Server Certificate'))
        extension_suites[0].append(crypto.X509Extension(b'subjectKeyIdentifier', False, b"hash", subject=subject))
        extension_suites[0].append(crypto.X509Extension(b'authorityKeyIdentifier', False, b"keyid:always,issuer:always",issuer=issuer))
        extension_suites[0].append(crypto.X509Extension(b'keyUsage', True, b"digitalSignature,keyEncipherment"))
        extension_suites[0].append(crypto.X509Extension(b'extendedKeyUsage',False, b"serverAuth"))
    elif cert_type =='ca':
        extension_suites[0].append(crypto.X509Extension(b'subjectKeyIdentifier', False, b"hash", subject=subject))
        extension_suites.append([])
        extension_suites[1].append(crypto.X509Extension(b'basicConstraints', True, b'CA:true'))
        extension_suites[1].append(crypto.X509Extension(b'authorityKeyIdentifier', False, b"keyid:always,issuer:always",issuer=issuer))
        extension_suites[1].append(crypto.X509Extension(b'keyUsage', True, b"digitalSignature,cRLSign,keyCertSign"))

    return extension_suites  
