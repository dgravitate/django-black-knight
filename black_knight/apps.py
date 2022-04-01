from django.apps import AppConfig
from django.db.models import Manager
from django.db.models.signals import class_prepared
from django.dispatch import receiver

from black_knight.managers import SelectRelatedManager


def register_class_prepared_receiver():
    @receiver(class_prepared)
    def replace_manager(sender, *args, **kwargs):
        if hasattr(sender, 'objects') and isinstance(sender.objects, Manager):
            if hasattr(sender.objects, 'clear_cache'):
                return sender
            sender._original_objects = sender.objects
            sender.objects = SelectRelatedManager()
            sender.objects.model = sender


class BlackKnightConfig(AppConfig):
    name = 'black_knight'
    verbose_name = 'Black Knight'

    def __init__(self, *args, **kwargs):
        register_class_prepared_receiver()
        super().__init__(*args, **kwargs)

    def ready(self) -> None:
        from . import receivers  # noqa

        from django.contrib.admin import site
        site.disable_action('delete_selected')
