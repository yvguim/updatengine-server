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

from inventory.models import entity, machine, net, software, osdistribution
from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.core.urlresolvers import reverse

class netInline(admin.TabularInline):
	model = net
	max_num = 0
        readonly_fields = ('manualy_created',)

class osInline(admin.TabularInline):
	model = osdistribution
	max_num = 0
        readonly_fields = ('manualy_created',)

class entityAdmin(admin.ModelAdmin):
	fields = ['name','description','parent']
	list_display = ('name','description','parent')
        ordering =('name',)

class machineAdmin(admin.ModelAdmin):
	fields = ['serial', 'name', 'manualy_created','vendor','product','entity','typemachine','timeprofile','packageprofile','packages']
	list_display = ('name','lastsave','serial','vendor','product','entity','typemachine','packageprofile','timeprofile', 'manualy_created')
	list_editable = ('entity','packageprofile','timeprofile')
	list_filter = ('entity','typemachine', 'manualy_created','timeprofile','packageprofile',
			('lastsave',DateFieldListFilter)
			)
      	search_fields = ('name', 'serial','vendor','product')
        readonly_fields = ('manualy_created',)
	inlines = [osInline, netInline]
	filter_horizontal = ('packages',)
        date_hierarchy = 'lastsave'
        ordering =('-lastsave',)

class netAdmin(admin.ModelAdmin):
	list_display = ('ip','mask','mac','machine', 'manualy_created')
	search_fields = ('ip','mask','mac','host__name')
	list_filter = ('manualy_created','host')
        readonly_fields = ('manualy_created',)
        ordering =('ip',)

	def machine(self, obj):
	        url = reverse('admin:inventory_machine_change', args=(obj.host.id,))
		return '<a href="%s">%s</a>' % (url, unicode(obj.host)) 
	machine.allow_tags = True


	def __init__(self, *args, **kwargs):
		super(netAdmin, self).__init__(*args, **kwargs)
		self.list_display_links = ('ip','machine', )



class osAdmin(admin.ModelAdmin):
	list_display = ('name','version','arch','systemdrive','host','manualy_created')
	search_fields = ('name','version','arch','systemdrive','host__name')
	list_filter = ('name','version','arch','systemdrive','host','manualy_created')
        readonly_fields = ('manualy_created',)
        ordering =('name',)

class softwareAdmin(admin.ModelAdmin):
	list_display = ('name','version', 'uninstall','machine','manualy_created')
	search_fields = ('name','version','host__name')
	list_filter = ('host','name','manualy_created')
        readonly_fields = ('manualy_created',)
        ordering =('name',)
	
	def machine(self, obj):
	        url = reverse('admin:inventory_machine_change', args=(obj.host.id,))
		return '<a href="%s">%s</a>' % (url, unicode(obj.host)) 
	machine.allow_tags = True


	def __init__(self, *args, **kwargs):
		super(softwareAdmin, self).__init__(*args, **kwargs)
		self.list_display_links = ('name','host', )

admin.site.register(osdistribution,osAdmin)
admin.site.register(machine, machineAdmin)
admin.site.register(entity, entityAdmin)
admin.site.register(net, netAdmin)
admin.site.register(software, softwareAdmin)
