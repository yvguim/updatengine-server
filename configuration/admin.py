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

from configuration.models import deployconfig
from django.contrib import admin

class deployconfigAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('name','activate_deploy','activate_time_deploy','start_time','end_time', 'entity', 'packageprofile', 'timeprofile')
    list_editable = ('activate_deploy','activate_time_deploy','start_time','end_time', 'entity', 'packageprofile', 'timeprofile')
    list_display_links = ('name',)

    readonly_fields = ('name',)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(deployconfig, deployconfigAdmin)
