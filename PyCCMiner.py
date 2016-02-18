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
import select
import socket
import sys
###########################################################################

if __name__ == "__main__":
    try:
        while True:
            parser = argparse.ArgumentParser(description='Process command-line arguements.')
            parser.add_argument('String', metavar='string',
                                    help='String to perform GET HTTP request on.')
            args = parser.parse_args()

            conn1 = socket.create_connection(('localhost', 4068))
            print('Connected!')
            conn1.send('GET '.encode('utf-8') + '/'.encode('utf-8') +
                            args.String.encode('utf-8') + ' HTTP/1.1'.encode('utf-8'))

            try:
                while True:
                    rlist, wlist, elist = select.select([conn1], [], [conn1], 5)

                    if rlist:
                        recvdata = conn1.recv(512).decode('utf-8')

                        if recvdata is not '':
                            for row in recvdata.split(';'):
                                print(row)
                        else:
                            break
                    if elist:
                        break

            except KeyboardInterrupt:
                print('Shutting down socket!')
                conn1.close()
                print('Socket shutdown!')
                sys.exit(2)

    except KeyboardInterrupt:
        print('Shutting down socket!')
        conn1.close()
        print('Socket shutdown!')
        sys.exit(2)


