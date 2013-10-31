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
from deploy.filters import entityFilter, machineFilter, statusFilter,\
        packageEntityFilter, packageHistoryFilter, conditionEntityFilter, conditionFilter
from inventory.models import entity
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib import messages

class ueAdmin(admin.ModelAdmin):
    list_max_show_all = 600
    list_per_page = 200
    actions_selection_counter = True
    list_select_related = True

    def get_export_as_csv_filename(self, request, queryset):
        return 'deploy'

class packageForm(ModelForm):
    class Meta:
        model = package

    # Custom form to be able to use request in clean method
    # http://stackoverflow.com/questions/1057252/how-do-i-access-the-request-object-or-any-other-variable-in-a-forms-clean-met/1057640#1057640
    # http://stackoverflow.com/questions/2683689/django-access-request-object-from-admins-form-clean
    def __init__(self, *args, **kwargs):
        self.my_user = kwargs.pop('my_user')
        super(packageForm, self).__init__(*args, **kwargs)
        self.fields['editor'].choices =([(self.my_user.id,self.my_user.username)])
        self.fields['editor'].widget.can_add_related = False
        if not self.my_user.is_superuser and self.fields.has_key('entity') and self.fields.has_key('conditions'):
            #restrict entity choice
            self.fields["entity"].queryset = entity.objects.filter(pk__in = self.my_user.subuser.id_entities_allowed).order_by('name').distinct() 
            self.fields["entity"].required = True
            # Restrict condition choice
            self.fields['conditions'].queryset = packagecondition.objects.filter(entity__pk__in = self.my_user.subuser.id_entities_allowed).\
                    order_by('name').distinct() 
        if self.fields.has_key('entity'):
            self.fields['entity'].widget.can_add_related = False

    def clean_editor(self):
        return self.my_user

    def clean(self):
        if self.instance and hasattr(self.instance, 'editor'):
            if not self.my_user.is_superuser and (self.instance.editor != self.my_user and self.instance.exclusive_editor == 'yes'):
                raise ValidationError('You cannot edit, save or delete this object. Ask %s to do it.' % self.instance.editor.username)
        return self.cleaned_data

class packageAdmin(ueAdmin):
    list_display = ('name','description','command','filename','get_conditions','ignoreperiod','public','editor','exclusive_editor')
    list_display_link = ('name')
    search_fields = ('name','description','command','filename','public')
    list_filter = ('ignoreperiod',packageEntityFilter,conditionFilter)
    filter_horizontal = ('conditions','entity')
    form = packageForm
    fieldsets = (
                (_('packageAdmin|general information'), {'fields': ('name', 'description')}),
                (_('packageAdmin|package edition'), {'fields': ('conditions', 'command', 'filename')}),
                (_('packageAdmin|permissions'), {'fields': ('public','ignoreperiod','entity','editor', 'exclusive_editor')}),
                )
    
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and (obj is not None and obj.editor != request.user and obj.exclusive_editor == 'yes'):
            return ['name','description','command','conditions','filename','ignoreperiod','public','exclusive_editor','entity'] 
        else:
            return []

    # Prevent deletion of objects when user hasn't enough permission
    def has_delete_permission(self, request, obj=None):
        if obj is not None: 
            return request.user.is_superuser or obj.editor == request.user or obj.exclusive_editor == 'no' 
        return True

    # Prevent to change objects when user hasn't enough permission
    def has_change_permission(self, request, obj=None):
        if obj is not None: 
            return request.user.is_superuser or obj.editor == request.user or obj.exclusive_editor == 'no' 
        else:
            return request.user.is_superuser or request.user.has_perm('deploy.change_package')

    def get_form(self, request, obj=None, **kwargs): 
        form = super(packageAdmin, self).get_form(request, obj, **kwargs) 
        # Custom form to be able to use request in clean method
        # http://stackoverflow.com/questions/1057252/how-do-i-access-the-request-object-or-any-other-variable-in-a-forms-clean-met/1057640#1057640
        # http://stackoverflow.com/questions/2683689/django-access-request-object-from-admins-form-clean
        class metaform(form):
            def __new__(cls, *args, **kwargs):
                kwargs['my_user'] = request.user
                return form(*args, **kwargs)
        if obj is not None and not request.user.is_superuser and (obj.editor != request.user and obj.exclusive_editor == 'yes'):
                messages.error(request,'An exclusive editor (%s) is set for this package, you will not be able to save your modification' % obj.editor.username)
        return metaform 
    
    def get_actions(self, request):
        actions = super(packageAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
            del actions['mass_update']
            del actions['export_as_csv']
        return actions

    def queryset(self, request):
        # Re-create queryset with entity list returned by list_entities_allowed
        if request.user.is_superuser:
            return package.objects.all()
        else:
            return package.objects.filter(entity__pk__in = request.user.subuser.id_entities_allowed)


class packagehistoryAdmin(ueAdmin):
    list_display = ('date','machine','status','name','description','command','filename','package')
    search_fields = ('status','name','description','command')
    list_filter = (entityFilter, machineFilter,packageHistoryFilter,statusFilter,
            ('date', DateFieldListFilter))
    ordering =('-date',)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return True

    def __init__(self, *args, **kwargs):
        super(packagehistoryAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )
    
    def queryset(self, request):
        # Re-create queryset with entity list returned by list_entities_allowed
        if request.user.is_superuser:
            return packagehistory.objects.all()
        else:
            return packagehistory.objects.filter(machine__entity__pk__in = request.user.subuser.id_entities_allowed)

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
    filter_horizontal = ('entity',)
    list_filter = (conditionEntityFilter,)
    fieldsets = (
            (_('packageAdmin|condition edition'), {'fields': ('name','depends', 'softwarename', 'softwareversion')}),
            (_('packageAdmin|permissions'), {'fields': ('entity',)}),
    )
    
    def get_form(self, request, obj=None): 
        form = super(packageconditionAdmin, self).get_form(request, obj) 
        if request.user.is_superuser:
            return form
        else:
            form.base_fields["entity"].queryset = entity.objects.filter(pk__in = request.user.subuser.id_entities_allowed).\
                    order_by('name').distinct() 
            form.base_fields["entity"].empty_label = None
            form.base_fields["entity"].required = True
        return form 

    def queryset(self, request):
        # Re-create queryset with entity list returned by list_entities_allowed
        if request.user.is_superuser:
            return packagecondition.objects.all()
        else:
            return packagecondition.objects.filter(entity__pk__in = request.user.subuser.id_entities_allowed)

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
