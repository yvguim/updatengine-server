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

from deploy.models import package, packagehistory, packageprofile, packagecondition, timeprofile, packagewakeonlan, impex
from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

class ueAdmin(admin.ModelAdmin):
    list_max_show_all = 600
    list_per_page = 200
    actions_selection_counter = True
    list_select_related = True

    def get_export_as_csv_filename(self, request, queryset):
        return 'deploy'

class packageAdmin(ueAdmin):
	list_display = ('name','description','command','filename','get_conditions','ignoreperiod','public')
	list_editable = ('ignoreperiod','public')
	search_fields = ('name','description','command','filename','public')
	list_filter = ('ignoreperiod',)
	filter_horizontal = ('conditions',)

class packagehistoryAdmin(ueAdmin):
	list_display = ('date','machine','status','name','description','command','filename','package')
	search_fields = ('status','name','description','command')
	list_filter = ('machine','package','status',
			('date', DateFieldListFilter))
	ordering =('-date',)
	def has_add_permission(self, request):
		return False
	def has_delete_permission(self, request, obj=None):
		return True

	def __init__(self, *args, **kwargs):
		super(packagehistoryAdmin, self).__init__(*args, **kwargs)
		self.list_display_links = (None, )

class packageprofileAdmin(ueAdmin):
	list_display = ('name','description', 'get_packages', 'parent')
	filter_horizontal = ('packages',)

class timeprofileAdmin(ueAdmin):
	list_display = ('name','description','start_time','end_time')
	search_fields = ('name','description')
	list_editable = ('start_time','end_time')

class wakeonlanAdmin(ueAdmin):
	list_display = ('name','description','date','status')
	search_fields = ('name','description')
	list_editable = ('date','status',)
	filter_horizontal = ('machines',)

class packageconditionAdmin(ueAdmin):
	list_display = ('name','depends','softwarename','softwareversion')

class impexAdmin(ueAdmin):
    list_display = ('date','name','description','filename_link','package')
    search_fields = ('name','description')
    readonly_fields = ('packagesum',)

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('filename', 'package')
        return self.readonly_fields
admin.site.register(packagewakeonlan, wakeonlanAdmin)
admin.site.register(timeprofile, timeprofileAdmin)
admin.site.register(packagecondition, packageconditionAdmin)
admin.site.register(packageprofile, packageprofileAdmin)
admin.site.register(packagehistory, packagehistoryAdmin)
admin.site.register(package, packageAdmin)
admin.site.register(impex, impexAdmin)
