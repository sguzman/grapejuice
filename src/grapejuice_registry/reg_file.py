import re


class RegistryType:
    def __init__(self, type_string):
        self.type_string = type_string

    def __repr__(self):
        return self.type_string

    def __hash__(self):
        return hash(self.type_string)


class UndefinedRegistryType(RegistryType):
    def __init__(self):
        super().__init__("undefined")


class DWORDRegistryType(RegistryType):
    def __init__(self):
        super().__init__("dword")


class StringRegistryType(RegistryType):
    def __init__(self):
        super().__init__("string")


class HexRegistryType(RegistryType):
    def __init__(self):
        super().__init__("hex")


def get_registry_value_type(value):
    dword_match = re.match(r"dword:(.+)", value)
    if dword_match:
        return DWORDRegistryType(), dword_match.group(1)

    hex_match = re.match(r"hex:(.+)", value)
    if hex_match:
        return HexRegistryType(), hex_match.group(1)

    string_match = re.match(r"\"(.*)?\"", value)
    if string_match:
        return StringRegistryType(), string_match.group(1)

    return UndefinedRegistryType(), value


registry_item_counter = 0


class RegistryItem:
    def __init__(self):
        global registry_item_counter
        self.serial_no = registry_item_counter
        registry_item_counter += 1

    def __hash__(self):
        return hash(self.serial_no)

    def __lt__(self, other):
        return self.serial_no < other.serial_no


class RegistryKey(RegistryItem):
    def __init__(self, key, timestamp):
        super().__init__()
        self.key = str(key)
        self.timestamp = int(timestamp)
        self.tags = []
        self.properties = []
        self.comments = []
        self.text_items = []
        self.ats = []

    def __repr__(self):
        return self.key

    def __hash__(self):
        my_hash = hash(super())
        my_hash ^= hash(self.key)
        my_hash ^= hash(self.timestamp)

        def hash_list(l, h):
            for item in l:
                h ^= hash(item)

            return h

        my_hash = hash_list(self.tags, my_hash)
        my_hash = hash_list(self.properties, my_hash)
        my_hash = hash_list(self.comments, my_hash)
        my_hash = hash_list(self.text_items, my_hash)
        my_hash = hash_list(self.ats, my_hash)

        return my_hash

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)


class RegistryTag(RegistryItem):
    def __init__(self, key, value):
        super().__init__()
        self.key = key
        self.value = value

    def __repr__(self):
        return "#" + self.key + "=" + self.value

    def __hash__(self):
        return hash(super()) ^ hash(self.key) ^ hash(self.value)


class RegistryAt(RegistryItem):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __hash__(self):
        return hash(super()) ^ hash(self.value)


class RegistryProperty(RegistryItem):
    def __init__(self, key, value):
        super().__init__()
        self.key = key
        self.type, self.value = get_registry_value_type(value)

    def __repr__(self):
        return self.key + " = " + repr(self.value)

    def __hash__(self):
        return hash(super()) ^ hash(self.key) ^ hash(self.value) ^ hash(self.type)


class RegistryComment(RegistryItem):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def __repr__(self):
        return ";; " + self.text

    def __hash__(self):
        return hash(super()) ^ hash(self.text)


class RegistryText(RegistryItem):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def __repr__(self):
        return self.text

    def __hash__(self):
        return hash(super()) ^ hash(self.text)


class RegFile:
    def __init__(self, p):
        self.global_key = RegistryKey("", 0)
        self.keys: [RegistryKey] = []
        read_reg(self, p)

    def to_dict(self):
        d = dict()
        for key in self.keys:
            d[key.key] = key

        return d


def read_reg(rf: RegFile, p: str):
    global registry_item_counter
    registry_item_counter = 0

    current_key = None

    with open(p) as file:
        for line in file.readlines():
            if not line:
                continue

            line = line.strip("\n")
            if not line:
                continue

            key_match = re.match(r"\[(.+)?]\s*(\d+)", line)
            if key_match:
                current_key = RegistryKey(key_match.group(1), key_match.group(2))
                rf.keys.append(current_key)
                continue

            property_match = re.match(r"\"(.+)?\"=(.+)", line)
            if property_match:
                if current_key:
                    prop = RegistryProperty(property_match.group(1), property_match.group(2))
                    current_key.properties.append(prop)
                continue

            tag_match = re.match(r"#(.+)?=(.*)", line)
            if tag_match:
                tag = RegistryTag(tag_match.group(1), tag_match.group(2))
                if current_key:
                    current_key.tags.append(tag)
                else:
                    rf.global_key.tags.append(tag)
                continue

            comment_match = re.match(r";;\s*(.*)", line)
            if comment_match:
                comment = RegistryComment(comment_match.group(1))
                if current_key:
                    current_key.comments.append(comment)
                else:
                    rf.global_key.comments.append(comment)
                continue

            at_match = re.match(r"@=(.+)", line)
            if at_match:
                at = RegistryAt(at_match.group(1))
                if current_key:
                    current_key.ats.append(at)
                else:
                    rf.global_key.ats.append(at)

            text = RegistryText(line)
            if current_key:
                current_key.text_items.append(text)
            else:
                rf.global_key.text_items.append(text)
