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
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.utils.encoding import force_unicode


class enableFilter(SimpleListFilter):
    title = _('Activate advanced filter')
    parameter_name = 'enablefilter'

    def lookups(self, request, model_admin):
        return [('True',_('yes')),]

    def queryset(self, request, queryset):
        return queryset

    def choices(self, cl):
        yield {
            'selected': self.value() is None,
            'query_string': cl.get_query_string({}, [self.parameter_name]),
            'display': _('no'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_unicode(lookup),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

class softwareFilter(SimpleListFilter):
   # Human-readable title which will be displayed in the
   # right admin sidebar just above the filter options.
   title = _('software')

   # Parameter for the filter that will be used in the URL query.
   parameter_name = 'softname'

   def lookups(self, request, model_admin):
       """
       Returns a list of tuples. The first element in each
       tuple is the coded value for the option that will
       appear in the URL query. The second element is the
       human-readable name for the option that will appear
       in the right sidebar.
       """
       if 'enablefilter' in request.GET:
           return software.objects.order_by('name').values_list('name','name').distinct()

   def queryset(self, request, queryset):
       """
       Returns the filtered queryset based on the value
       provided in the query string and retrievable via
       `self.value()`.
       """
       if self.value() is not None:
           if 'softversion' in request.GET:
               return queryset.filter(software__name__iexact=self.value(), software__version__iexact=request.GET['softversion'])
           else:
               return queryset.filter(software__name__iexact=self.value())
       else:
           return queryset

class versionFilter(SimpleListFilter):
   # Human-readable title which will be displayed in the
   # right admin sidebar just above the filter options.
   title = _('softversion')

   # Parameter for the filter that will be used in the URL query.
   parameter_name = 'softversion'

   def lookups(self, request, model_admin):
       """
       Returns a list of tuples. The first element in each
       tuple is the coded value for the option that will
       appear in the URL query. The second element is the
       human-readable name for the option that will appear
       in the right sidebar.
       """

       if 'softname' in request.GET:
          return software.objects.filter(name__iexact=request.GET['softname'] ).order_by('version').values_list('version','version').distinct()

   def queryset(self, request, queryset):
       """
       Returns the filtered queryset based on the value
       provided in the query string and retrievable via
       `self.value()`.
       """
       if self.value() is not None:
           return queryset.filter(software__name__iexact=request.GET['softname'], software__version__iexact=self.value())
       else:
           return queryset

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

class entityAdmin(ueAdmin):
    fields = ['name','description','parent','packageprofile','force_packageprofile','timeprofile','force_timeprofile']
    list_display = ('name','description','parent','packageprofile','force_packageprofile','timeprofile','force_timeprofile')
    list_editable = ('packageprofile','force_packageprofile','timeprofile','force_timeprofile')
    ordering =('name',)

def force_contact(modeladmin, request, queryset):
    import socket, time
    Sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # definition des informations :
    Port = 2010
    for machine in queryset:
        try:
            for netcard in net.objects.filter(host=machine):
                if netcard.ip != '127.0.0.1':
                    Sock.connect((netcard.ip,Port))
                    Sock.send(machine.softsum)
                    Sock.close()
                    time.sleep(3)
        except:
            pass
force_contact.short_description = _('force_inventory')

class machineAdmin(ueAdmin):
    select_related = True
    fields = ['name', 'serial','uuid','domain','language', 'vendor','product','manualy_created','entity','typemachine','timeprofile','packageprofile','packages']
    list_display = ('lastsave','name','serial','domain','vendor','product','entity','typemachine','packageprofile','timeprofile')
    list_editable = ('entity','packageprofile','timeprofile')
    list_filter = (('lastsave', DateFieldListFilter), 'entity','domain','language','typemachine', 'timeprofile','packageprofile', enableFilter,softwareFilter, versionFilter)
    search_fields = ('name', 'serial','vendor','product','domain','language')
    readonly_fields = ('typemachine', 'manualy_created',)
    inlines = [osInline, netInline, softInline]
    filter_horizontal = ('packages',)
    date_hierarchy = 'lastsave'
    ordering =('-lastsave',)
    actions = [force_contact]

class netAdmin(ueAdmin):
    list_display = ('ip','mask','mac','host')
    search_fields = ('ip','mask','mac','host__name')
    list_filter = ('host',)
    readonly_fields = ('manualy_created',)
    ordering =('ip',)


class osAdmin(ueAdmin):
    list_display = ('name','version','arch','systemdrive','host')
    search_fields = ('name','version','arch','systemdrive','host__name')
    list_filter = ('name','version','arch','systemdrive','host')
    readonly_fields = ('manualy_created',)
    ordering =('name',)


class softwareAdmin(ueAdmin):
    list_display = ('name','version','host')
    search_fields = ('name','version','host__name')
    list_filter = ('host',)
    readonly_fields = ('manualy_created',)
    ordering =('name',)


admin.site.register(osdistribution,osAdmin)
admin.site.register(machine, machineAdmin)
admin.site.register(entity, entityAdmin)
admin.site.register(net, netAdmin)
admin.site.register(software, softwareAdmin)
