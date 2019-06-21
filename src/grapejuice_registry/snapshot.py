import json
import os
import re
import time
import uuid
from datetime import datetime
from zipfile import ZipFile

from grapejuice_common import variables

cached_snapshot_index = None


class Snapshot:
    loaded = False

    def __init__(self, pfx_id, snapshot_id=None):
        if snapshot_id is None:
            snapshot_id = str(uuid.uuid4())

        self.metadata = {
            "id": snapshot_id,
            "name": "Untitled snapshot",
            "description": "Snapshot created at " + str(datetime.now()),
            "pfx_id": pfx_id,
            "timestamp": int(time.time()),
            "broken": False
        }

    def __lt__(self, other):
        if isinstance(other, Snapshot):
            return self.timestamp > other.timestamp

        return False

    @property
    def id(self):
        return self.metadata["id"]

    @property
    def filename(self):
        return self.id + ".zip"

    @property
    def metadata_filename(self):
        return self.id + ".metadata.json"

    @property
    def name(self):
        return self.metadata["name"] or "Untitled snapshot"

    @name.setter
    def name(self, value):
        self.metadata["name"] = str(value)

    @property
    def description(self):
        return self.metadata["description"] or "The description for this snapshot was lost"

    @description.setter
    def description(self, value):
        self.metadata["description"] = str(value)

    @property
    def pfx_id(self):
        return self.metadata["pfx_id"] or "undefined"

    @pfx_id.setter
    def pfx_id(self, value):
        self.metadata["pfx_id"] = value

    @property
    def timestamp(self):
        return self.metadata["timestamp"] or int(time.time())

    @property
    def datetime(self):
        return datetime.utcfromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def broken(self):
        value = self.metadata["broken"]
        if value is None:
            value = False

        return value

    @broken.setter
    def broken(self, value):
        self.metadata["broken"] = value

    def create(self, source_list: [(str, str)]):
        p_zip = os.path.join(variables.sparklepop_snapshots_dir(), self.filename)
        with ZipFile(p_zip, "w") as z:
            for name, p_file in source_list:
                z.write(p_file, name)

        self.save_metadata()

    def _metadata_path(self):
        return os.path.join(variables.sparklepop_snapshots_dir(), self.metadata_filename)

    def save_metadata(self):
        with open(self._metadata_path(), "w+") as f_metadata:
            self.metadata["archive"] = self.filename
            pretty_json_dump(self.metadata, f_metadata)

        if not self.loaded:
            snapshot_index_append(self.pfx_id, self.id)

    def load(self):
        with open(self._metadata_path(), "r") as f_metadata:
            self.loaded = True
            self.metadata = json.load(f_metadata)

    def update(self):
        self.save_metadata()


def pretty_json_dump(obj: dict, fp):
    json.dump(obj, fp, sort_keys=True, indent=4)


def generate_pfx_metadata():
    return {
        "id": str(uuid.uuid4())
    }


def fill_metadata_gaps(target: dict, source: dict) -> bool:
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


def current_pfx_metadata() -> dict:
    p = os.path.join(variables.wineprefix_dir(), "sparklepop.metadata.json")
    if not os.path.exists(p):
        metadata = generate_pfx_metadata()
        with open(p, "w+") as file:
            json.dump(metadata, file)
    else:
        with open(p, "r") as file:
            metadata = json.load(file)

    if fill_metadata_gaps(metadata, generate_pfx_metadata()):
        with open(p, "w+") as file:
            json.dump(metadata, file)

    return metadata


def snapshot_index_path():
    return os.path.join(variables.sparklepop_config_dir(), "snapshot_index.json")


def snapshot_index():
    global cached_snapshot_index
    if cached_snapshot_index is not None:
        return cached_snapshot_index

    p_index = snapshot_index_path()
    if os.path.exists(p_index):
        with open(p_index, "r") as index_file:
            index = json.load(index_file)
    else:
        index = {
            "last_updated": int(time.time()),
            "snapshots": {}
        }

        with open(p_index, "w+") as index_file:
            pretty_json_dump(index, index_file)

    cached_snapshot_index = index
    return index


def save_snapshot_index(index):
    index["last_updated"] = int(time.time())
    with open(snapshot_index_path(), "w+") as file:
        pretty_json_dump(index, file)

    global cached_snapshot_index
    cached_snapshot_index = index


def snapshot_index_append(pfx_id, snap_id):
    index = snapshot_index()

    if pfx_id in index["snapshots"].keys():
        snap_object = index["snapshots"][pfx_id]
    else:
        snap_object = {}
        index["snapshots"][pfx_id] = snap_object

    if "snapshots" in snap_object.keys():
        snap_array = snap_object["snapshots"]
    else:
        snap_array = []
        snap_object["snapshots"] = snap_array

    snap_array.append(snap_id)
    snap_object["last_updated"] = int(time.time())
    save_snapshot_index(index)


def create_snapshot():
    reg_files = []
    pfx_basepath = variables.wineprefix_dir()
    for file in os.listdir(pfx_basepath):
        if re.match(r"^.+?\.reg", file):
            reg_files.append((file, os.path.join(pfx_basepath, file)))

    snapshot = Snapshot(current_pfx_metadata()["id"])
    snapshot.create(reg_files)
