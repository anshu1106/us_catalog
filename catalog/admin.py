from django.contrib import admin

from .models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import FieldListFilter
from django.utils.safestring import mark_safe
import csv
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
# Register your models here.

def makeRangeFieldListFilter(lookups, nullable=False):
    class RangeFieldListFilter(FieldListFilter):
        def __init__(self, field, request, params, model, model_admin, field_path):
            self.field_generic = '%s__' % field_path
            self.range_params = dict([(k, v) for k, v in params.items()
                                     if k.startswith(self.field_generic)])

            self.lookup_kwarg_start = '%s__gte' % field_path
            self.lookup_kwarg_stop = '%s__lt' % field_path
            self.lookup_kwarg_null = '%s__isnull' % field_path

            self.links = [ (_('Any value'), {}), ]
            for name, start, stop in lookups:
                query_params = {}
                if start is not None:
                    query_params[self.lookup_kwarg_start] = str(start)
                if stop is not None:
                    query_params[self.lookup_kwarg_stop] = str(stop)

                self.links.append((name, query_params))

            if nullable:
                self.links.append((_('Unknown'), {
                    self.lookup_kwarg_null: 'True'
                }))

            super(RangeFieldListFilter, self).__init__(
                field, request, params, model, model_admin, field_path)

        def expected_parameters(self):
            return [
                self.lookup_kwarg_start,
                self.lookup_kwarg_stop,
                self.lookup_kwarg_null
            ]

        def choices(self, cl):
            for title, param_dict in self.links:
                yield {
                    'selected': self.range_params == param_dict,
                    'query_string': cl.get_query_string(
                                        param_dict, [self.field_generic]),
                    'display': title,
                }

    return RangeFieldListFilter

def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    
	    def export_as_csv(modeladmin, request, queryset):
	        """
	        Generic csv export admin action.
	        based on http://djangosnippets.org/snippets/1697/
	        """
	        opts = modeladmin.model._meta
	        field_names = set([field.name for field in opts.fields])
	        if fields:
	            fieldset = set(fields)
	            field_names = field_names & fieldset
	        elif exclude:
	            excludeset = set(exclude)
	            field_names = field_names - excludeset

	        response = HttpResponse(content_type='text/csv')
	        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

	        writer = csv.writer(response)
	        if header:
	            writer.writerow(list(field_names))
	        for obj in queryset:
	            writer.writerow([unicode(getattr(obj, field)).encode("utf-8","replace") for field in field_names])
	        return response
	    export_as_csv.short_description = description
	    return export_as_csv

	    export_as_csv.short_description = description
	    return export_as_csv



class CatalogAdmin(admin.ModelAdmin):
    list_display = (
        'brand', 'category', 'item_name', 'max_retail_price','client_price','photo','image_tag')
    readonly_fields = ('image_tag',)
    actions = [export_as_csv_action("CSV Export", fields=['brand', 'category', 'item_name', 'max_retail_price','client_price','photo','image_tag',])]
    #fields = ( 'image_tag', )
	#readonly_fields = ('image_tag',)
    list_filter = ('brand','category',
    ('max_retail_price', makeRangeFieldListFilter([
            (_('Less than 100'), None, 100),
            (_('100 to 500'), 100, 500),
            (_('500 to 1000'), 500, 1000),
            (_('1000 to 7500'), 1000, 7500),
            (_('7500 to 15000'), 7500, 15000),
            (_('15000 to 30000'), 15000, 30000),
            (_('At least 30000'), 30000, None),
        ], nullable=True)) )
	
    # search_fields = ['user__username', 'phone']

	
   


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Catalog, CatalogAdmin)

    