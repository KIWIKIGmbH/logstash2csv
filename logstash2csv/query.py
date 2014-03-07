from parser import Logstash2CSVJSON


class Logstash2CSVQuery(object):
    def load_query_file(self, query_file):
        self._query = Logstash2CSVJSON.load_json_file(query_file)

    def load_query(self, query):
        self._query = Logstash2CSVJSON.load_json(query)

    def set_range_of_timestamp(self, from_time):
        self._range_of_timestamp()["from"] = from_time

    def _range_of_timestamp(self):
        filter = self._query["query"]["filtered"]["filter"]
        return filter["bool"]["must"][0]["range"]["@timestamp"]

    def query(self):
        return self._query
