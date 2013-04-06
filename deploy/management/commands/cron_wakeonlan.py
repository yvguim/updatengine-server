###################################################################################
# UpdatEngine - Software Packages Deployment and Administration tool              #  
#                                                                                 #
# Copyright (C) Yves Guimard - yves.guimard@gmail.com                             #
#                                                                                 #
# This program is free software; you can redistribute it and/or                   #
# modify it under the terms of the GNU General Public License                     #
# as published by the Free Software Foundation; either version 2                  #
# of the License, or (at your option) any later version.                          #
#                                                                                 #
# This program is distributed in the hope that it will be useful,                 #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                  #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   #
# GNU General Public License for more details.                                    #
#                                                                                 #
# You should have received a copy of the GNU General Public License               #
# along with this program; if not, write to the Free Software                     #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA. #
###################################################################################

from django.core.management.base import BaseCommand
from deploy.models import packagewakeonlan
from inventory.models import net
from datetime import datetime
from time import sleep
from django.utils.timezone import utc
import struct, socket

def wake_on_lan(ethernet_address):

  # Construct a six-byte hardware address

  addr_byte = ethernet_address.split(':')
  hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
    int(addr_byte[1], 16),
    int(addr_byte[2], 16),
    int(addr_byte[3], 16),
    int(addr_byte[4], 16),
    int(addr_byte[5], 16))

  # Build the Wake-On-LAN "Magic Packet"...

  msg = '\xff' * 6 + hw_addr * 16

  # ...and send it to the broadcast address using UDP

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  s.sendto(msg, ('<broadcast>', 9))
  sleep(1)
  s.sendto(msg, ('<broadcast>', 7))
  s.close()


class Command(BaseCommand):
	def handle(self, *args, **options):
		now = datetime.utcnow().replace(tzinfo=utc)
		for package in packagewakeonlan.objects.filter(status='Programmed', date__lt= now):
			for machine in package.machines.all():
				for netcard in net.objects.filter(host=machine):
					print 'Wakeonlan of '+machine.name+' Mac: '+netcard.mac
					wake_on_lan(str(netcard.mac))
					
				sleep(5)
			package.status = 'Completed'
			package.save()
