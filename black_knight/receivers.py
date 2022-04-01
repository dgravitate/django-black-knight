import inspect

from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations import AddField, AlterField
from django.db.models import ForeignKey, ForeignObject, Manager
from django.db.models.signals import pre_delete, pre_migrate, class_prepared
from django.dispatch import receiver

from black_knight.mixins import DeletableModelMixin



DELETABLE_MODEL_TYPES = (DeletableModelMixin, ContentType, MigrationRecorder.Migration)
ALLOWED_ON_DELETE_METHODS = ('PROTECT',)  # TODO: allow override in settings
ALTER_METHODS = (AddField, AlterField,)


@receiver(pre_delete)
def block_deletes_by_default(sender, instance, using, *args, **kwargs):
    # TODO: see if we can figure out if this is a single object or QuerySet
    # TODO: add a setting to bypass this
    # TODO: add a force_delete to allow deleting if you really really mean it
    if not isinstance(instance, DELETABLE_MODEL_TYPES):
        raise IntegrityError("Deletes are not allowed")


@receiver(pre_migrate)
def block_destructive_on_delete_methods(sender, app_config, verbosity, interactive, using, plan, apps, *args, **kwargs):
    for migration, is_rolled_back in plan:
        if not is_rolled_back:
            for operation in migration.operations:
                if isinstance(operation, ALTER_METHODS):
                    if isinstance(operation.field, (ForeignKey, ForeignObject,)):  # FIXME: make sure we're looking at all the right Rel classes
                        on_delete_method = operation.field.remote_field.on_delete.__name__
                        if on_delete_method not in ALLOWED_ON_DELETE_METHODS:
                            raise IntegrityError(f"on_delete method {on_delete_method} is not allowed!")



