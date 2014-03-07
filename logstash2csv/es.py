from elasticsearch import Elasticsearch


class Es(object):
    def __init__(self, setting):
        self._es = Elasticsearch([setting])

    def search(self, index, body):
        self.res = self._es.search(index=index, body=body)

    def hits(self):
        return self.res["hits"]["hits"]
