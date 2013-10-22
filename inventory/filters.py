from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from inventory.models import software

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

class as_or_notFilter(SimpleListFilter):
    title = _('As software or not?')
    parameter_name = 'asornot'

    def lookups(self, request, model_admin):
        if 'enablefilter' in request.GET:
            return [('True',_('as_not_software')),]
        else:
            return

    def queryset(self, request, queryset):
        return queryset

    def choices(self, cl):
        yield {
            'selected': self.value() is None,
            'query_string': cl.get_query_string({}, [self.parameter_name]),
            'display': _('as_software'),
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
         else:
             return
    
    def queryset(self, request, queryset):
         """
         Returns the filtered queryset based on the value
         provided in the query string and retrievable via
         `self.value()`.
         """
         if 'asornot' in request.GET and 'enablefilter' in request.GET:
             if self.value() is not None:
                 if 'softversion' in request.GET:
                     if software.objects.filter(version__iexact=request.GET['softversion'], name__iexact=self.value()).exists():
                         return queryset.exclude(software__version__iexact=request.GET['softversion'], software__name__iexact=self.value())
                     else:
                         return queryset.exclude(software__name__iexact=self.value())
                 else:
                     return queryset.exclude(software__name__iexact=self.value())
         elif 'enablefilter' in request.GET: 
             if self.value() is not None:
                 if 'softversion' in request.GET:
                     if software.objects.filter(version__iexact=request.GET['softversion'], name__iexact=self.value()).exists():
                         return queryset.filter(software__name__iexact=self.value(), software__version__iexact=request.GET['softversion'])
                     else:
                         return queryset.filter(software__name__iexact=self.value())
                 else:
                     return queryset.filter(software__name__iexact=self.value())
             else:
                 return queryset
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

        if 'enablefilter' in request.GET:
            if 'softname' in request.GET:
                return software.objects.filter(name__iexact=request.GET['softname'] ).order_by('version').values_list('version','version').distinct()
        else:
            return
   def queryset(self, request, queryset):
       """
       Returns the filtered queryset based on the value
       provided in the query string and retrievable via
       `self.value()`.
       """
       return queryset

