import json
import os
import pytest
from datetime import datetime, timedelta

from logstash2csv import Logstash2CSV


class TestLogstash2CSV(object):
    def pytest_funcarg__client(request):
        return Logstash2CSV()

    def test_load_connection(self, client):
        client.load_connection(self.path("files/connection.json"))

        assert client.connection() == self.sample_conn()

    def test_set_connection(self, client):
        client.set_connection(
            {
                "host": "test.example.org",
                "port": 443,
                "basic_auth": {
                    "user": "user",
                    "password": "password"
                },
                "use_ssl": True
            }
        )

        assert client.connection() == self.sample_conn()

    def test_load_fields(self, client):
        client.load_fields(self.path("files/fields.json"))
        fields = client.fields()

        for f in self.sample_fields():
            assert f in fields

    def test_set_fields(self, client):
        client.set_fields(self.sample_fields())
        fields = client.fields()

        for f in self.sample_fields():
            assert f in fields

    def test_set_query(self, client):
        client.set_query(self.sample_query())
        q = client.query()

        should = q["query"]["filtered"]["query"]["bool"]["should"]
        range = q["query"]["filtered"]["filter"]["bool"]["must"][0]["range"]
        size = q["size"]
        sort = q["sort"][0]

        assert should[0]["query_string"]["query"] == "query_string"
        assert range["@timestamp"]["from"] == 1393766754482
        assert range["@timestamp"]["to"] == "now"
        assert size == 500
        assert sort["@timestamp"]["order"] == "desc"

    def test_set_output_fields(self, client):
        client.load_fields(self.path("files/fields.json"))

        client.set_output_fields(["@timestamp", "_id", "_index"])
        assert client.output_fields() == ["@timestamp", "_id", "_index"]

        client.set_output_fields(["@timestamp", "", "_index"])
        assert client.output_fields() == ["@timestamp", "_index"]

        client.set_output_fields(["", "", ""])
        assert client.output_fields() == client.fields()

    def test_set_range(self, client):
        client.set_query(self.sample_query())
        from_datetime = client.set_range(term=3600*24*3)

        q = client.query()
        range = q["query"]["filtered"]["filter"]["bool"]["must"][0]["range"]
        assert from_datetime == range["@timestamp"]["from"]

    def test_set_index(self, client):
        client.set_index(ds=3)
        format = "logstash-%Y.%m.%d"

        today = datetime.today().strftime(format)
        yesterday = (datetime.today() - timedelta(1)).strftime(format)
        day_before_yesterday = (
            datetime.today() - timedelta(2)).strftime(format)
        index = ",".join([today, yesterday, day_before_yesterday])

        assert client.index() == index

    def path(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def sample_conn(self):
        return {
            "host": "test.example.org",
            "port": 443,
            "http_auth": "user:password",
            "use_ssl": True
        }

    def sample_fields(self):
        return ["@timestamp", "_id", "_index"]

    def sample_query(self):
        return json.dumps({
            "query": {
                "filtered": {
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "query_string": {
                                        "query": "query_string"
                                    }
                                }
                            ]
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    "range": {
                                        "@timestamp": {
                                            "from": 1393766754482,
                                            "to": "now"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            },
            "size": 500,
            "sort": [
                {
                    "@timestamp": {
                        "order": "desc"
                    }
                }
            ]
        })

if __name__ == "__main__":
    pytest.main()
