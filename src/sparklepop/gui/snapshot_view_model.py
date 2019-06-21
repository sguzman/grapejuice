from grapejuice_registry import snapshot


class PrefixModel(list):
    def __init__(self, id: str, timestamp: int):
        super().__init__()
        self.id = id
        self.timestamp = timestamp

    def __lt__(self, other):
        if isinstance(other, PrefixModel):
            return self.timestamp > other.timestamp

        return False


class SnapshotViewModel(list):
    def __init__(self):
        super().__init__()

        index = snapshot.snapshot_index()
        snapshots_table = index["snapshots"]
        for pfx_id, pfx_object in snapshots_table.items():
            pfx = PrefixModel(pfx_id, pfx_object["last_updated"])

            for snap_id in pfx_object["snapshots"]:
                snap = snapshot.Snapshot(pfx_id, snap_id)
                snap.load()
                pfx.append(snap)

            pfx.sort()
            self.append(pfx)

        self.sort()
