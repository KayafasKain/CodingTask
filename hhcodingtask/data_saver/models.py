from django.contrib.postgres.fields import JSONField
from django.db import models

from .utils import validate_flexible_model


class GenericModel(models.Model):
    data = JSONField()

    def __str__(self):
        return self.data

    def save(
        self, force_insert=False, force_update=False, using=None,
        update_fields=None,
    ):
        validate_flexible_model(self.data, self.__class__.__name__)

        super(GenericModel, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
