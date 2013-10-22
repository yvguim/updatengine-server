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
from django.utils.translation import ugettext_lazy as _
from inventory.filters import enableFilter, as_or_notFilter, softwareFilter, versionFilter

class ueAdmin(admin.ModelAdmin):
    list_max_show_all = 600
    list_per_page = 100
    actions_selection_counter = True
    list_select_related = True

    def get_export_as_csv_filename(self, request, queryset):
        return 'inventory'

class netInline(admin.TabularInline):
    model = net
    max_num = 5000
    extra = 0
    readonly_fields = ('manualy_created',)

class osInline(admin.TabularInline):
    model = osdistribution
    max_num = 5000
    extra = 0
    readonly_fields = ('manualy_created',)

class softInline(admin.TabularInline):
    model = software
    max_num = 10000
    extra = 0
    readonly_fields = ('name', 'version', 'uninstall', 'manualy_created',)
    # Uncomment when django bug number #20807 will be fixed
    #def has_add_permission(self, request):
    #            return False

class entityAdmin(ueAdmin):
    fields = ['name','description','parent','packageprofile','force_packageprofile','timeprofile','force_timeprofile']
    list_display = ('name','description','parent','packageprofile','force_packageprofile','timeprofile','force_timeprofile')
    list_editable = ('packageprofile','force_packageprofile','timeprofile','force_timeprofile')
    ordering =('name',)

    def queryset(self, request):
        # Re-create queryset with entity list returned by list_entities_allowed
        return entity.objects.filter(pk__in = request.user.subuser.id_entities_allowed)

class machineAdmin(ueAdmin):
    select_related = True
    fields = ['name', 'serial','uuid','domain','username','language', 'vendor','product','manualy_created','entity','typemachine','timeprofile','packageprofile','packages']
    list_display = ('lastsave','entity','name','domain','username','vendor','product','typemachine','packageprofile','timeprofile')
    list_editable = ('entity','packageprofile','timeprofile')
    list_filter = (('lastsave', DateFieldListFilter), 'entity','domain','username','language','typemachine','osdistribution__name', 'timeprofile','packageprofile', enableFilter, as_or_notFilter, softwareFilter, versionFilter)
    search_fields = ('name', 'serial','vendor','product','domain','username','language')
    readonly_fields = ('typemachine', 'manualy_created',)
    inlines = [osInline, netInline, softInline]
    filter_horizontal = ('packages',)
    date_hierarchy = 'lastsave'
    ordering =('-lastsave',)
    actions = ['force_contact', 'force_wakeup']

    def queryset(self, request):
        # Re-create queryset with entity list returned by list_entities_allowed
        return machine.objects.filter(entity__pk__in = request.user.subuser.id_entities_allowed)
   
    def force_wakeup(self, request, queryset):
        for machine in queryset:
            machine.wakeup()
    force_wakeup.short_description = _('force_wakeup')

    def force_contact(modeladmin, request, queryset):
        for machine in queryset:
            machine.force_contact()
    force_contact.short_description = _('force_inventory')

class netAdmin(ueAdmin):
    list_display = ('ip','mask','mac','host')
    search_fields = ('ip','mask','mac','host__name')
    list_filter = ('host',)
    readonly_fields = ('manualy_created',)
    ordering =('ip',)

    def queryset(self, request):
        return net.objects.filter(host__entity__pk__in = request.user.subuser.id_entities_allowed)

class osAdmin(ueAdmin):
    list_display = ('name','version','arch','systemdrive','host')
    search_fields = ('name','version','arch','systemdrive','host__name')
    list_filter = ('name','version','arch','systemdrive','host')
    readonly_fields = ('manualy_created',)
    ordering =('name',)

    def queryset(self, request):
        return osdistribution.objects.filter(host__entity__pk__in = request.user.subuser.id_entities_allowed)

class softwareAdmin(ueAdmin):
    list_display = ('name','version','host')
    search_fields = ('name','version','host__name')
    list_filter = ('host',)
    readonly_fields = ('manualy_created',)
    ordering =('name',)

    def queryset(self, request):
        return software.objects.filter(host__entity__pk__in = request.user.subuser.id_entities_allowed)

admin.site.register(osdistribution,osAdmin)
admin.site.register(machine, machineAdmin)
admin.site.register(entity, entityAdmin)
admin.site.register(net, netAdmin)
admin.site.register(software, softwareAdmin)
