###############################################################################
#!    This program is free software: you can redistribute it and/or modify
#!    it under the terms of the GNU General Public License as published by
#!    the Free Software Foundation, either version 3 of the License, or
#!    (at your option) any later version.

#!    This program is distributed in the hope that it will be useful,
#!    but WITHOUT ANY WARRANTY; without even the implied warranty of
#!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#!    GNU General Public License for more details.

#!    You should have received a copy of the GNU General Public License
#!    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!    Copyright Cody Ferber, 2016.
###############################################################################
from contextlib import closing
import argparse
import datetime
import io
import select
import socket
import sys

###############################################################################
class Client():
###############################################################################
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
#       print(exception_type)
#       print(exception_value)
#       print(traceback)
        return True

###############################################################################
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process command-line.')
        parser.add_argument('-c', metavar='string', required=False,
                                help='GET HTTP request command.')
        parser.add_argument('-v', action="store_true", required=False,
                                help='Verbose to log.txt.')
        self.args = parser.parse_args()

        print('Loading PyCCMiner.ini.')
        self.HOST = Client.getCfg(self, '[HOST]')
        self.PORT = Client.getCfg(self, '[PORT]')
        self.LOG  = Client.getCfg(self, '[LOG]')
        print('Connecting: ' + self.HOST + ':' + self.PORT)

        if self.args.v is True:
            print('Verbose: ' + self.LOG)

###############################################################################
    def doLog(self, input):
        if self.args.v is True:
            with closing(open(self.LOG, 'a')) as file:
                for row in input.splitlines():
                    file.write('[{:%Y-%m-%d:%H:%M:%S}] '.format(
                                    datetime.datetime.now()) + row + '\n')

###############################################################################
    def getCfg(self, cfgvar):
        with closing(open('PyCCMiner.ini', 'r')) as file:
            buffer = file.read(None).splitlines()
            cfgvar = buffer.pop(buffer.index(cfgvar) + 1)
            return cfgvar

###############################################################################
    def Connect(self):
        while True:
            if self.args.c is None:
                command = input('> ')
            else:
                command = self.args.c

            with closing(socket.create_connection((self.HOST, self.PORT))) as conn1:
                conn1.send('GET '.encode('utf-8') + '/'.encode('utf-8') +
                                command.encode('utf-8') + ' HTTP/1.1'.encode('utf-8'))

                rlist, wlist, elist = select.select([conn1], [], [], 5)
                if rlist:
                    recvdata = conn1.recv(1024).decode('utf-8')
                    if recvdata is not '':
                        for row in recvdata.split(';'):
                            print(row)
                            Client.doLog(self, row)
                    else:
                        conn1.shutdown()

###############################################################################
if __name__ == "__main__":
    with Client() as client:
        client.Connect()
