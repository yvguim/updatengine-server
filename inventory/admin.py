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


class ueAdmin(admin.ModelAdmin):
    list_max_show_all = 600
    list_per_page = 200
    actions_selection_counter = True
    list_select_related = True      
    
    def get_export_as_csv_filename(self, request, queryset):
        return 'inventory'

class netInline(admin.TabularInline):
    model = net
    max_num = 0
    readonly_fields = ('manualy_created',)


class osInline(admin.TabularInline):
    model = osdistribution
    max_num = 0
    readonly_fields = ('manualy_created',)

class softInline(admin.TabularInline):
    model = software
    max_num = 0
    readonly_fields = ('name', 'version', 'uninstall', 'manualy_created',)

class entityAdmin(ueAdmin):
    fields = ['name','description','parent']
    list_display = ('name','description','parent')
    ordering =('name',)


class machineAdmin(ueAdmin):
    select_related = True
    fields = ['name', 'serial', 'vendor','product','manualy_created','entity','typemachine','timeprofile','packageprofile','packages']
    list_display = ('lastsave','name','serial','vendor','product','entity','typemachine','packageprofile','timeprofile', 'manualy_created')
    list_editable = ('entity','packageprofile','timeprofile')
    list_filter = ('entity','typemachine', 'manualy_created','timeprofile','packageprofile',
            ('lastsave',DateFieldListFilter)
            )
    search_fields = ('name', 'serial','vendor','product')
    readonly_fields = ('typemachine', 'manualy_created',)
    inlines = [osInline, netInline, softInline]
    filter_horizontal = ('packages',)
    date_hierarchy = 'lastsave'
    ordering =('-lastsave',)


class netAdmin(ueAdmin):
    list_display = ('ip','mask','mac','host', 'manualy_created')
    search_fields = ('ip','mask','mac','host__name')
    list_filter = ('manualy_created','host')
    readonly_fields = ('manualy_created',)
    ordering =('ip',)


class osAdmin(ueAdmin):
    list_display = ('name','version','arch','systemdrive','host','manualy_created')
    search_fields = ('name','version','arch','systemdrive','host__name')
    list_filter = ('name','version','arch','systemdrive','host','manualy_created')
    readonly_fields = ('manualy_created',)
    ordering =('name',)


class softwareAdmin(ueAdmin):
    list_display = ('name','version', 'uninstall','host','manualy_created')
    search_fields = ('name','version','host__name')
    list_filter = ('host','manualy_created')
    readonly_fields = ('manualy_created',)
    ordering =('name',)
    

admin.site.register(osdistribution,osAdmin)
admin.site.register(machine, machineAdmin)
admin.site.register(entity, entityAdmin)
admin.site.register(net, netAdmin)
admin.site.register(software, softwareAdmin)
