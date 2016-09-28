import sys
PY2 = sys.version_info[0] == 2

if PY2:
    from urllib2 import urlopen, URLError, HTTPError
else:
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError

class tileInfo():

    class Info:
        """Class collecting some information about the content located at the
        given URL.

        :param url: Valid URL to the website *(e.g.
                    http://example.com/path/to/file.html)*.
        """
        def __init__(self, url):
            self._url = url

            # Open URL and catch exceptions
            try:
                self._site = urlopen(self._url)
            except HTTPError as e:
                self._site = e
            except URLError as e:
                raise URLError(e.reason)

            # Process the file-like object we got
            if PY2:
                self._content = self._site.read()
            else:
                # Try multiple encodings
                for codec in ["utf-8", "utf-16", "utf-32",
                              "latin-1", "cp1251", "ascii"]:
                    try:
                        self._content = self._site.read().decode(codec)
                        # Decoding successful, break look
                        break
                    except UnicodeDecodeError:
                        # Decoding failed, try another one
                        continue

        @property
        def content(self):
            """Get the url's content.

            :return: Content of the url *(e.g. HTML code)*.
            :rtype: str
            """
            return self._content

        @property
        def content_type(self):
            """Get the url's content type.

            :return: Content-type of the url's code *(e.g. image/jpeg )*.
            :rtype: str or NoneType
            """
            return self._site.info()["Content-Type"]

