from grapejuice_registry.reg_file import RegFile, RegistryKey


class RegDiff:
    def __init__(self, baseline: RegFile, other: RegFile):
        self.baseline: RegFile = baseline
        self.other: RegFile = other

        self.additions: [RegistryKey] = []
        self.removals: [RegistryKey] = []
        self.changes: [(RegistryKey, RegistryKey)] = []

    def do_diff(self):
        baseline = self.baseline.to_dict()
        other = self.other.to_dict()
        all_keys = set()
        add_keys = []
        removal_keys = []
        change_keys = []

        for key, reg_key in baseline.items():
            if key not in other.keys():
                removal_keys.append(key)
                all_keys.add(key)

        for key, reg_key in other.items():
            if key not in baseline.keys():
                add_keys.append(key)
                all_keys.add(key)

        for key in removal_keys:
            all_keys.remove(key)

        for key in add_keys:
            all_keys.remove(key)

        for key in all_keys:
            if baseline[key] != other[key]:
                change_keys.append(key)

        for key in add_keys:
            self.additions.append(other[key])

        for key in removal_keys:
            self.removals.append(baseline[key])

        for key in change_keys:
            self.changes.append((baseline[key], other[key]))


if __name__ == "__main__":
    import os

    broken = os.path.join(os.environ["HOME"], ".local/share/grapejuice", "wineprefix-broken/user.reg")
    working = os.path.join(os.environ["HOME"], ".local/share/grapejuice", "wineprefix-working/user.reg")

    diff = RegDiff(RegFile(broken), RegFile(working))
    diff.do_diff()
    debug = 0
