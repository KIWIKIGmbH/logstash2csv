import json


class Logstash2CSVJSON(object):
    @classmethod
    def load_json_file(cls, json_file):
        with open(json_file, "r") as f:
            return json.load(f)

    @classmethod
    def load_json(cls, json_string):
        return json.loads(json_string)
