import json


from django import forms

from .models import GenericModel
from .utils import get_form_fields


class FlexibleForm(forms.ModelForm):

    def __init__(self, *args, instance=None, **kwargs):
        super(FlexibleForm, self).__init__(*args, instance=instance, **kwargs)

        if instance:
            initials = json.loads(instance.data)
        else:
            initials = {}

        self._extra_fields = get_form_fields(initials)

        self.fields.update(self._extra_fields)

    def save(self, commit=True):
        if hasattr(self, 'data'):
            self.instance.data = json.dumps(
                {
                    field_name: self.cleaned_data[field_name]
                    for field_name in self._extra_fields.keys()
                }
            )

        return super(FlexibleForm, self).save(commit)

    class Meta:
        model = GenericModel
        fields = []
