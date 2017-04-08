class UrlParse():
    def __init__(self, url):
        self._url_split = [x for x in url.split('/') if x]
        self._url = url

    def __str__(self):
        return self._url

    def __repr__(self):
        return self._url

    def __hash__(self):
        return hash(self._url)

    def __eq__(self, other):
        other_url_split = [x for x in other.split('/') if x]
        if len(self._url_split) != len(other_url_split):
            return False
        for squerry, oquerry in zip(self._url_split, other_url_split):
            if squerry[0] != ':' and squerry != oquerry:
                return False
        return True

a = UrlParse('/plugins/:id/enable')

mydict = {'GET': {a: 'func', UrlParse('/plugins/hell'): 'func2'}}

print(mydict['GET'].get('/plugins/hell'))