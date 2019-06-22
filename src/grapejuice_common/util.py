import os


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
