import json


class ISerializable():
    def __init__():
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)