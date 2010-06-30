###    This program is free software: you can redistribute it and/or modify
###    it under the terms of the GNU General Public License as published by
###    the Free Software Foundation, either version 3 of the License, or
###    (at your option) any later version.
###
###    This program is distributed in the hope that it will be useful,
###    but WITHOUT ANY WARRANTY; without even the implied warranty of
###    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
###    GNU General Public License for more details.

###    You should have received a copy of the GNU General Public License
###    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import android, math, xmpp
from time import sleep
droid = android.Android()
droid.startLocating()
sleep(15)
location = droid.readLocation().result
droid.stopLocating()

#Replace with your long in credentials

USERNAME = "gtalk user name"
PASSWORD = "gtalk password"
RESOURCE = "gmail.com"

from xmpp import *

#set up xmpp client
cl=Client(server='gmail.com',debug=[])

if not cl.connect(server=('talk.google.com',5222)):
	raise IOError('Can not connect to server.')
if not cl.auth(USERNAME, PASSWORD, RESOURCE):
    raise IOError('Can not auth with server.')

#calculate the distance between two gps locations
def distance(location1, location2, radius=1):
    R = 6371
    latitude1 = math.radians(location1['latitude'])
    latitude2 = math.radians(location2['latitude'])
    longitude1 = math.radians(location1['longitude'])
    longitude2 = math.radians(location2['longitude'])
    distance = math.acos(math.sin(latitude1) * math.sin(latitude2) + math.cos(latitude1) * math.cos(latitude2) * math.cos(longitude2-longitude1)) * R

#return true if distance is less than 1k
    if distance < radius:
        return True
    else:
        return False
message = ''
#add your own gps coordinants and status messages here
places = (("Yay I'm Home!", {'latitude':0.00 'longitude':0.00}),
            ('Stuck at Work', {'latitude':0.00, 'longitude':0.00}))

#check if you are at one of the locations in your places list
for place in places:
    if distance(place[1], location['gps']):
        message = place[0]

#if you arn't at one of your locations set your status to this
if not message:
    message = 'Out and about'

#update the status
cl.send(Iq('set','google:shared-status', payload=[
		Node('show',payload=['default']),
		Node('status',payload=[message])
]))
cl.disconnect()
droid.notify('Status Updated', message)
