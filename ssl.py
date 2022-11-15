
import datetime
rt datetime
import socket
import ssl
import OpenSSL
def get_num_days_before_expired(hostname: str, port: str = '443') -> int:
    """
    Get number of days before an TLS/SSL of a domain expired
    """
    cert = ssl.get_server_certificate((hostname, int(port)))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    expiry_date = datetime.datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%S%z')
    delta = expiry_date - datetime.datetime.now(datetime.timezone.utc)
    print(f'{hostname} expires in {delta.days} day(s)')
    return delta.days
