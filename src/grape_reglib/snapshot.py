import json
import os
import uuid

from grape_common import variables


def generate_metadata():
    return {
        "id": str(uuid.uuid4())
    }


def fill_metadata_gaps(target: dict, source: dict):
    modified = False

    for k in source.keys():
        if k in target.keys():
            if type(source[k]) != type(target[k]):
                del target[k]

    for k in source.keys():
        if k not in target.keys():
            target[k] = source[k]
            modified = True

    return modified


def current_metadata():
    p = os.path.join(variables.wineprefix_dir(), "sparklepop.metadata.json")
    if not os.path.exists(p):
        metadata = generate_metadata()
        with open(p, "w+") as file:
            json.dump(metadata, file)
    else:
        with open(p, "r") as file:
            metadata = json.load(file)

    if fill_metadata_gaps(metadata, generate_metadata()):
        with open(p, "w+") as file:
            json.dump(metadata, file)

    return metadata
