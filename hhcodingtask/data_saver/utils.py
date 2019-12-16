import json
from functools import partial

from django import forms
from django.conf import settings

form_field_options = {
    float: forms.FloatField,
    int: forms.IntegerField,
    str: partial(forms.CharField, max_length=100),
}


def get_form_fields(initials=None):
    return {
        name: form_field_options[type_](
            initial=initials.get(name) if initials else None,
        )
        for name, type_ in settings.FLEXIBLE_FORM.items()
    }


def validate_flexible_model(data, model_name):
    for name, value in json.loads(data).items():
        assert name in settings.FLEXIBLE_FORM, \
            'Field "%s" not specified for "%s"' % (name, model_name)
        assert settings.FLEXIBLE_FORM[name] == type(value), \
            'Wrong values provided for field: "%s", expected: %s' % (
                name, settings.FLEXIBLE_FORM[name],
            )
