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

from configuration.models import deployconfig, subuser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

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

class subuserInline(admin.TabularInline):
    model = subuser
    filter_horizontal = ('entity',)
    
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return True

class UserAdmin(UserAdmin):

    #redefine get_form method to display subuserInline only on edit page
    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
            'form': self.add_form,
            'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
            })
        else:
            self.inlines = (subuserInline,)
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    fieldsets = (
                (None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                # Removing the permission part
                (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'user_permissions')}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
                # Keeping the group parts? Ok, but they shouldn't be able to define
                # their own groups, up to you...
                (_('Groups'), {'fields': ('groups',)}),
		)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(deployconfig, deployconfigAdmin)
