import os

import requests


def prepare_uri(uri):
    if uri is None:
        return None

    if os.path.exists(uri):
        return uri

    prepared_uri = uri.replace("'", "")
    if prepared_uri:
        return prepared_uri
    else:
        return None


def download_file(url, target_path):
    response = requests.get(url)
    assert 199 < response.status_code < 300, f"Got status {response.status_code} for {url}"

    with open(target_path, "wb+") as fp:
        fp.write(response.content)

    return target_path
