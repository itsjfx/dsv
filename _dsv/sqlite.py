import argparse
import subprocess
from ._base import _Base

class sqlite(_Base):
    ''' use sql on the data '''
    parser = argparse.ArgumentParser()
    parser.add_argument('sql', nargs='+')
    parser.add_argument('-t', '--table', default='input')

    DELIM = b'\t'

    def __init__(self, opts):
        super().__init__(opts)
        self.proc = None
        if self.opts.no_header:
            self.opts.parser.error('Cannot use -N/--no-header with sqlite')

    def start_proc(self):
        if not self.proc:
            self.proc = subprocess.Popen([
                'sqlite3', '-csv', '-header',
                '-separator', self.DELIM,
                '-cmd', f'.import /dev/stdin {self.opts.table}',
                '-cmd', ' '.join(self.opts.sql),
            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def on_header(self, header):
        self.on_row(header)

    def on_row(self, row):
        self.start_proc()
        self.proc.stdin.write(self.DELIM.join(self.format_columns(row, self.DELIM, b'\n', True)) + b'\n')

    def on_eof(self):
        if self.proc:
            self.proc.stdin.close()
            self.opts.ifs = self.DELIM
            list(_Base(self.opts).process_file(self.proc.stdout))
            self.proc.wait()
