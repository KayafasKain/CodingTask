from django.contrib import admin

from .forms import FlexibleForm
from .utils import get_form_fields
from .models import GenericModel


class GenericModelAdmin(admin.ModelAdmin):
    form = FlexibleForm

    def get_fields(self, request, obj=None):
        gf = super(GenericModelAdmin, self).get_fields(request, obj)

        self.form.declared_fields.update(get_form_fields())

        return gf


admin.site.register(GenericModel, GenericModelAdmin)
