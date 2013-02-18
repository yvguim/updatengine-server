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

from django.utils.translation import ugettext_lazy as _
from django.db import models

class entity(models.Model):
	name = models.CharField(max_length=100,verbose_name = _('entity|name'))
	description = models.TextField(max_length=1000,verbose_name = _('entity|description'))
	parent = models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.SET_NULL,verbose_name = _('entity|parent'))

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('entity|entity')
		verbose_name_plural = _('entity|entities')

class typemachine (models.Model):
	name = models.CharField(max_length=100, verbose_name = _('typemachine|name'))
	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name = _('typemachine|typemachine')
		verbose_name_plural = _('typemachine|typesofmachines')

class machine(models.Model):
	choice = (
			('yes', _('yes')),
			('no', _('no'))
		)
	serial = models.CharField(max_length=100, verbose_name = _('machine|serial'))
	name = models.CharField(max_length=100, verbose_name = _('machine|name'))
	vendor = models.CharField(max_length=100,null=True, blank=True, default='undefined',verbose_name = _('machine|vendor'))
	product = models.CharField(max_length=100,null=True, blank=True, default='undefined',verbose_name = _('machine|product'))
	entity = models.ForeignKey(entity,null=True, blank=True, on_delete=models.SET_NULL, verbose_name = _('machine|entity'))
	packageprofile = models.ForeignKey('deploy.packageprofile',null=True, blank=True, on_delete=models.SET_NULL, verbose_name = _('machine|package profile'), help_text= _('machine|packages profile help text'))
	timeprofile = models.ForeignKey('deploy.timeprofile',null=True, blank=True, on_delete=models.SET_NULL, verbose_name = _('machine|time deploy profile'))
	lastsave = models.DateTimeField(auto_now=True, verbose_name = _('machine|lastsave'))
	typemachine = models.ForeignKey(typemachine, null=True, blank=True, on_delete=models.SET_NULL, verbose_name = _('machine|typemachine'))
	netsum = models.CharField(max_length=40, null = True, blank=True, verbose_name = _('machine|netsum'))
	ossum = models.CharField(max_length=40, null = True, blank=True, verbose_name = _('machine|ossum'))
	softsum = models.CharField(max_length=40, null = True, blank=True, verbose_name = _('machine|softsum'))
	packages = models.ManyToManyField('deploy.package',null = True, blank = True, verbose_name = _('machine|packages'), help_text= _('machine|packages help text'))
	manualy_created = models.CharField(max_length=3, choices=choice, default='yes', verbose_name = _('machine|manualy_created'))

	class Meta:
		verbose_name = _('machine|machine')
		verbose_name_plural = _('machine|machines')

        def get_pack_from_profile(self):
                return "\n".join([p.name for p in self.packageprofile.packages.all()])

	def __unicode__(self):
		return self.name

class osdistribution(models.Model):
	choice = (
			('yes', _('yes')),
			('no', _('no'))
		)
	name = models.CharField(max_length=100, verbose_name = _('osdistribution|name'))
	version = models.CharField(max_length=100, null = True, blank = True, default = 'undefined', verbose_name = _('osdistribution|version'))
	arch = models.CharField(max_length=100, null = True, blank = True, verbose_name = _('osdistribution|arch'))
	systemdrive = models.CharField(max_length=100, null = True, blank = True, verbose_name = _('osdistribution|systemdrive'))
	host = models.ForeignKey(machine, verbose_name = _('osdistribution|host'))
	manualy_created = models.CharField(max_length=3, choices=choice, default='yes', verbose_name = _('osdistribution|manualy_created'))

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('osdistribution|osdistribution')
		verbose_name_plural = _('osdistribution|osdistributions')



class net(models.Model):
	choice = (
			('yes', _('yes')),
			('no', _('no'))
		)
	ip = models.CharField(max_length=50, verbose_name = _('net|ip'))
	mask = models.CharField(max_length=50, verbose_name = _('net|mask'))
	mac = models.CharField(max_length=100, verbose_name = _('net|mac'))
	host = models.ForeignKey(machine, verbose_name = _('net|host'))
	manualy_created = models.CharField(max_length=3, choices=choice, default='yes', verbose_name = _('net|manualy_created'))

	def __unicode__(self):
		return self.ip

	class Meta:
		verbose_name = _('net|network')
		verbose_name_plural = _('net|networks')



class software(models.Model):
	choice = (
			('yes', _('yes')),
			('no', _('no'))
		)
	name = models.CharField(max_length=100, verbose_name = _('software|name'))
	version = models.CharField(max_length=500,null=True, blank=True, default='undefined', verbose_name = _('software|version'))
	uninstall = models.CharField(max_length=500,null=True, blank=True, default='undefined', verbose_name = _('software|uninstall'))
	host = models.ForeignKey(machine, verbose_name = _('software|host'))
	manualy_created = models.CharField(max_length=3, choices=choice, default='yes', verbose_name = _('software|manualy_created'))

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('software|software')
		verbose_name_plural = _('software|softwares')

	@staticmethod
	def autocomplete_search_fields():
		return("name__iexact", "name__icontains",)

