import ssl
import sys
import os
import logging
import crlite_python
from pathlib import Path
from cryptography import x509
from cryptography.hazmat.primitives import serialization

def main():

	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	logger_handler = logging.StreamHandler(sys.stdout)
	logger_handler.setLevel(logging.DEBUG)
	logger_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
	logger.addHandler(logger_handler)

	db_dir = Path('/tmp/crlite_testing/crlite_db/')
	if not os.path.exists(db_dir):
		os.makedirs(db_dir)

	db = crlite_python.load_crlite_db(db_dir, update = True)

	revoked_cert_pem = ssl.get_server_certificate(('revoked.badssl.com', 443))
	valid_cert_pem = ssl.get_server_certificate(('rit.edu', 443))
	revoked_cert_x509 = x509.load_pem_x509_certificate(revoked_cert_pem.encode())
	valid_cert_x509 = x509.load_pem_x509_certificate(valid_cert_pem.encode())
	valid_cert_der = valid_cert_x509.public_bytes(serialization.Encoding.DER)
	revoked_cert_der = revoked_cert_x509.public_bytes(serialization.Encoding.DER)
	print(db.check_revocation_x509(revoked_cert_x509))
	print(db.check_revocation_x509(valid_cert_x509))
	print(db.check_revocation_x509_pem(revoked_cert_pem.encode()))
	print(db.check_revocation_x509_pem(valid_cert_pem.encode()))
	print(db.check_revocation_x509_der(revoked_cert_der))
	print(db.check_revocation_x509_der(valid_cert_der))

if __name__ == '__main__':
	main()