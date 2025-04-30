import click
import yaml
import zipfile
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa


@click.command()
@click.argument('domain')
@click.argument('filename', type=click.Path(exists=True))
def main(domain, filename):
    """
    Generate private keys, CSRs, and public keys for hosts defined in a YAML file.

    The YAML file should have the following structure:

    hosts:
      - name: cavendish
      - name: bigmike

    For each host, a fully qualified domain name (FQDN) is constructed by
    appending the domain (e.g. "test.niwc.navy.mil") to the host name.

    The script creates:
      - A CSR with subject "/CN={{ FQDN }}/OU=USN/OU=PKI/OU=DoD/O=U.S. Government/C=US"
      - An RSA private key (2048-bit)
      - A public key extracted from the private key

    Finally, three zip files are created in the current directory:
      - private_keys.zip (files named FQDN.key)
      - csrs.zip (files named FQDN.csr)
      - public_keys.zip (files named FQDN.pub)
    """
    # Load YAML file
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)

    if not data or 'hosts' not in data:
        click.echo("Error: YAML file must contain a 'hosts' key with a list of hosts.", err=True)
        return

    # Dictionaries to store file contents keyed by filename
    private_keys = {}
    csrs = {}
    public_keys = {}

    # Process each host entry
    for host in data['hosts']:
        host_name = host.get('name')
        if not host_name:
            click.echo("Warning: Skipping an entry without a 'name' field.", err=True)
            continue

        fqdn = f"{host_name}.{domain}"
        click.echo(f"Generating credentials for {fqdn} ...")

        # Generate RSA private key (2048 bits)
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Build the subject: /CN={{ fqdn }}/OU=USN/OU=PKI/OU=DoD/O=U.S. Government/C=US
        subject = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, fqdn),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "USN"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "PKI"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "DoD"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "U.S. Government"),
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        ])

        # Build the CSR with a SAN extension containing the FQDN
        csr_builder = x509.CertificateSigningRequestBuilder().subject_name(subject)
        san = x509.SubjectAlternativeName([x509.DNSName(fqdn)])
        csr_builder = csr_builder.add_extension(san, critical=False)
        csr = csr_builder.sign(key, hashes.SHA256())

        # Serialize private key in PEM format (unencrypted)
        key_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

        # Serialize CSR in PEM format
        csr_pem = csr.public_bytes(serialization.Encoding.PEM)

        # Extract and serialize public key in PEM format
        pub_key_pem = key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # Save files in dictionaries (filenames use the FQDN with appropriate extension)
        private_keys[f"{fqdn}.key"] = key_pem
        csrs[f"{fqdn}.csr"] = csr_pem
        public_keys[f"{fqdn}.pub"] = pub_key_pem

    # Create zip archives for the outputs
    create_zip("private_keys.zip", private_keys)
    create_zip("csrs.zip", csrs)
    create_zip("public_keys.zip", public_keys)

    click.echo("Zip files created: private_keys.zip, csrs.zip, public_keys.zip")


def create_zip(zip_filename: str, files: dict[str, bytes]) -> None:
    """
    Create a zip file with the given filename.

    Parameters:
      zip_filename: Name of the output zip file.
      files: A dictionary mapping filenames to file content (bytes).
    """
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for filename, content in files.items():
            zipf.writestr(filename, content)


if __name__ == '__main__':
    main()
