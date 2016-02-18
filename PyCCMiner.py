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

#!    Copyright Cody Ferber, 2013.
###########################################################################
import select
import sys
import socket

###########################################################################

conn1 = socket.create_connection(('localhost', 4068))
print('Connected!')
conn1.send('GET /summary HTTP'.encode('utf-8'))

try:	
    while True:
        rlist, wlist, elist = select.select([conn1.fileno()], [], [], 5)

        for conn in rlist:

            recvdata = conn1.recv(512)
            recvdata = recvdata.decode('utf-8')

            if recvdata is '':

                print('Client not sending data! Disconnecting!')
                sys.exit(1)

            else:
                print('Received: ' + recvdata)

except KeyboardInterrupt:
    sys.exit(2)
