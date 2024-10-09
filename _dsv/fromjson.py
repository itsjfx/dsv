import json
import argparse
from ._base import _Base

class fromjson(_Base):
    ''' convert from json '''

    def process_file(self, file):
        self.determine_delimiters(b'')

        for line in file:
            row = json.loads(line)
            if isinstance(row, dict):
                if self.header is None:
                    self.header = [x.encode('utf8') for x in row.keys()]
                    if self.on_header(self.header):
                        break
                row = [row.get(k.decode('utf8'), '') for k in self.header]
                row = [(x if isinstance(x, str) else json.dumps(x)).encode('utf8') for x in row]
                if self.on_row(row):
                    break
        self.on_eof()
        return ()
