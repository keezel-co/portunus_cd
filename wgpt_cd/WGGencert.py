from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import timedelta, datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_cert_signed_with_ca(subject, ca_cert_pem, ca_key_pem, key_size=2048):
    try:
        ca_cert_pem = Path(ca_cert_pem).read_bytes()
        ca_key_pem = Path(ca_key_pem).read_bytes()
    except:
        return False

    print(ca_key_pem)
    print(ca_cert_pem)
    ca_cert = x509.load_pem_x509_certificate(ca_cert_pem, default_backend())
    ca_key = load_pem_private_key(ca_key_pem, password=None, backend=default_backend())

    # Generate our key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )

    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, subject)
    ])

    alt_names = x509.SubjectAlternativeName([
        x509.DNSName(subject),
    ])

    # path_len=0 means this cert can only sign itself, not other certs.
    basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
    now = datetime.utcnow()

    cert_builder = x509.CertificateBuilder()

    cert = (
        cert_builder
            .subject_name(name)
            .issuer_name(ca_cert.subject)
            .public_key(key.public_key())
            .serial_number(1000)
            .not_valid_before(now)
            .not_valid_after(now + timedelta(days=100 * 365))
            .add_extension(basic_contraints, False)
            .add_extension(alt_names, False)
            .sign(ca_key, hashes.SHA256(), default_backend())
    )

    cert_der = cert.public_bytes(encoding=serialization.Encoding.DER)

    key_der = key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    ca_der = ca_cert.public_bytes(encoding=serialization.Encoding.DER)

    return cert_der, key_der, ca_der
