import logging

import certifi
import urllib3 as u3

HTTP = None

LOG = logging.getLogger(__name__)


def http():
    global HTTP

    if HTTP is None:
        HTTP = u3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where()
        )

        LOG.debug("Configured HTTP pool manager")

    return HTTP
