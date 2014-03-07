from parser import Logstash2CSVJSON


class Logstash2CSVConfig(object):
    _index_format = "logstash-%Y.%m.%d"

    def index_format(self):
        return self._index_format

    def load_connection_file(self, file):
        self._load_connection(Logstash2CSVJSON.load_json_file(file))

    def load_connection(self, conn):
        self._load_connection({"connection": conn})

    def load_fields_file(self, file):
        self._load_fields(Logstash2CSVJSON.load_json_file(file))

    def load_fields(self, fields):
        self._load_fields({"fields": fields})

    def load_output_fields(self, fields):
        trimed_fields = self._trim(fields)
        if not len(trimed_fields) > 0:
            self._output_fields = self._fields
        else:
            self._output_fields = trimed_fields

    def _load_connection(self, conf):
        if "connection" in conf:
            conn = conf["connection"]
            conn["http_auth"] = "%s:%s" % (
                conn["basic_auth"]["user"], conn["basic_auth"]["password"])
            del conn["basic_auth"]
            self._connection = conn

    def _load_fields(self, conf):
        if "fields" in conf:
            self._fields = self._trim(conf["fields"])

    def _trim(self, list):
        return filter(lambda x: x != "", list)

    def connection(self):
        return self._connection

    def fields(self):
        return self._fields

    def output_fields(self):
        if hasattr(self, "_output_fields"):
            return self._output_fields
        else:
            return self._fields
