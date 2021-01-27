# #!/usr/bin/env python3
# import swimlane_environment_validator.lib.config as config
# import swimlane_environment_validator.lib.log_handler as log_handler

# import OpenSSL.crypto
# from Crypto.Util import asn1

# logger = log_handler.setup_logger()

# def verify_certificate_key(certificate_path, key_path):

#     if not (certificate_path or key_path):
#         logger.info("One of the certificate arguments are not specified, not verifying certificate key pair")
#         return True

#     c=OpenSSL.crypto
    
#     # The certificate - an X509 object
#     try:
#         cert = OpenSSL.crypto.load_certificate(
#                  OpenSSL.crypto.FILETYPE_PEM, 
#                  open(certificate_path).read()
#                )
#     except:
#         logger.info("Couldn't open {}, the file path my not exist, or it may not be an X509-encoded certificate.".format(certificate_path))
    
#     # The private key - a PKey object
#     try:
#         priv = OpenSSL.crypto.load_privatekey(
#                  OpenSSL.crypto.FILETYPE_PEM, 
#                  open(key_path).read()
#                )
#     except:
#         logger.info("Couldn't open {}, the file path my not exist, or it may not be an X509-encoded certificate.".format(key_path))

#     pub = cert.get_pubkey()
    
#     # Only works for RSA (I think)
#     if pub.type()!=c.TYPE_RSA or priv.type()!=c.TYPE_RSA:
#         raise Exception('Can only handle RSA keys')
    
#     # This seems to work with public as well
#     pub_asn1=c.dump_privatekey(c.FILETYPE_ASN1, pub)
#     priv_asn1=c.dump_privatekey(c.FILETYPE_ASN1, priv)
    
#     # Decode DER
#     pub_der=asn1.DerSequence()
#     pub_der.decode(pub_asn1)
#     priv_der=asn1.DerSequence()
#     priv_der.decode(priv_asn1)
    
#     # Get the modulus
#     pub_modulus=pub_der[1]
#     priv_modulus=priv_der[1]
    
#     if pub_modulus==priv_modulus:
#         logger.info('{} key matches {}'.format(key_path, certificate_path))
#         return True
#     else:
#         logger.info('{} key does not match {}'.format(key_path, certificate_path))
#         return True