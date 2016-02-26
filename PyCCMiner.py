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
            with open(LOG, 'a') as file:
                for row in input.splitlines():
                    file.write('{:%Y-%m-%d:%H:%M:%S}: '.format(
                                    datetime.datetime.now()) + row + '\n')
                file.close()

        except IOError:
            print('IOError: ' + LOG)
            sys.exit(0)

###########################################################################

def getCfg(i):
    try:
        with open('PyCCMiner.ini', 'r') as file:
            buffer = file.read(None).splitlines()
            cfgvar = buffer.pop(i).split('=')
            file.close()
            return cfgvar.pop(1)
        
    except IOError:
        print('IOError: PyCCMiner.ini')
        sys.exit(0)

###########################################################################

if __name__ == "__main__":
    HOST = getCfg(0)
    PORT = getCfg(1)
    LOG  = getCfg(2)

    try:
        while True:
            parser = argparse.ArgumentParser(description='Process command-line.')
            parser.add_argument('-c', metavar='string', required=False,
                                    help='GET HTTP request command.')
            parser.add_argument('-o', action="store_true", required=False,
                                    help='Log to output.txt.')
            args = parser.parse_args()

            if args.c is None:
                command = input('> ')
            else:
                command = args.c

            conn1 = socket.create_connection((HOST, PORT))
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
                    conn1.close()
            if elist:
                break

    except ConnectionError:
        print('ConnectionError: ' + HOST + ':' + PORT + '!')
        sys.exit(0)

    except EOFError:
        sys.exit(0)
				
    except KeyboardInterrupt:
        sys.exit(0)
