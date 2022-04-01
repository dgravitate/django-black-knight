from django.db.models import Manager, ForeignObject, OneToOneRel


class SelectRelatedManager(Manager):
    def get_select_related_fields(self, *args, **kwargs):
        if hasattr(self.model, 'select_related_fields'):
            return self.model.select_related_fields

        select_related_fields = []
        for fk_field in self.model._meta.get_fields():
            if fk_field.name == 'history':   # bypass our history field for now
                continue

            if isinstance(fk_field, (ForeignObject, OneToOneRel)):
                select_related_fields.append(fk_field.name)
        return select_related_fields

    def get_queryset(self, *args, **kwargs):
        select_related_fields = self.get_select_related_fields(*args, **kwargs)
        return super().get_queryset(*args, **kwargs).select_related(*select_related_fields)
