###########################################################################
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
###########################################################################

import argparse
import datetime
import io
import select
import socket
import sys

###########################################################################

def doLog(input):
    if args.o is True:
        try:
            with open('output.txt', 'a') as file:
                for row in input.splitlines():
                    file.write('{:%Y-%m-%d:%H:%M:%S}: '.format(datetime.datetime.now()) + row + '\n')

        finally:
            file.close()

if __name__ == "__main__":
    while True:
        parser = argparse.ArgumentParser(description='Process command-line arguements.')
        parser.add_argument('-c', metavar='string', required=False,
                                help='GET HTTP request command.')
        parser.add_argument('-o', action="store_true", required=False,
                                help='Log to output.txt.')
        args = parser.parse_args()

        if args.c is None:
            command = input('> ')
        else:
            command = args.c

        try:
            conn1 = socket.create_connection(('localhost', 4068))
            conn1.send('GET '.encode('utf-8') + '/'.encode('utf-8') +
                            command.encode('utf-8') + ' HTTP/1.1'.encode('utf-8'))

            rlist, wlist, elist = select.select([conn1], [], [conn1], 5)

            if rlist:
                recvdata = conn1.recv(1024).decode('utf-8')
                if recvdata is not '':
                    for row in recvdata.split(';'):
                        print(row)
                        doLog(row)
                else:
                    break
            if elist:
                break

        except KeyboardInterrupt:
            sys.exit(0)

        finally:
            conn1.close()
