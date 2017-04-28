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

    def __eq__(self, other_str):
        other_url_split = [x for x in other_str.split('/') if x]
        if len(self._url_split) != len(other_url_split):
            return False
        for squerry, oquerry in zip(self._url_split, other_url_split):
            if squerry[0] != ':' and squerry != oquerry:
                return False
        return True

    def get_url_var(self, other_str):
        other_split = [x for x in other_str.split('/') if x]
        url_vars = {}
        for squerry, oquerry in zip(self._url_split, other_split):
            if squerry[0] == ':':
                url_vars[squerry[1:]] = oquerry

        return url_vars
