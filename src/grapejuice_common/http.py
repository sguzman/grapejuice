import certifi
import urllib3 as u3

HTTP = None


def http():
    global HTTP

    if HTTP is None:
        HTTP = u3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where()
        )

    return HTTP
