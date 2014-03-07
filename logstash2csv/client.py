from datetime import datetime, timedelta

from config import Logstash2CSVConfig
from es import Es
from query import Logstash2CSVQuery


class Logstash2CSV(object):
    def __init__(self):
        self._conf = Logstash2CSVConfig()
        self._query = Logstash2CSVQuery()
        self.set_index()

    def load_connection(self, file):
        self._conf.load_connection_file(file)

    def set_connection(self, conn):
        self._conf.load_connection(conn)

    def load_fields(self, file):
        self._conf.load_fields_file(file)

    def set_fields(self, fields):
        self._conf.load_fields(fields)

    def set_query(self, query):
        self._query.load_query(query)

    def set_output_fields(self, fields):
        self._conf.load_output_fields(fields)

    def set_range(self, term=0):
        if term == 0:
            from_datetime = datetime.today()
            ds = 30
        else:
            from_datetime = datetime.today() - timedelta(0, term)
            self._query.set_range_of_timestamp(from_datetime)
            ds = term/3600/24

        self.set_index(ds=ds)
        return from_datetime

    def set_index(self, ds=7):
        format = self._conf.index_format()
        today = datetime.today()
        self._index = ",".join(
            [(today - timedelta(d)).strftime(format) for d in range(ds)])

    def index(self):
        return self._index

    def query(self):
        return self._query.query()

    def connection(self):
        return self._conf.connection()

    def fields(self):
        return self._conf.fields()

    def output_fields(self):
        return self._conf.output_fields()

    def search(self):
        self._es = Es(self.connection())
        self._es.search(index=self.index(), body=self.query())

    def render_csv(self, separator=","):
        return "\n".join([separator.join(c) for c in self._generate_csv()])

    def _generate_csv(self):
        fields = self.output_fields()
        hits = self._es.hits()
        csv = [fields[:]]
        for h in hits:
            row = [str(self._get_value(h, f)) for f in fields]
            csv.append(row)

        return csv

    def _get_value(self, hit, field):
        try:
            value = hit["_source"][field]
        except:
            try:
                value = hit[field]
            except:
                value = ""
        finally:
            return value
