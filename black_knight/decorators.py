from django.utils.decorators import classonlymethod


def allow_user(**kwargs):
    def wrapper(class_view):
        def as_view(cls, **init_kwargs):
            view = super(cls, cls).as_view(**init_kwargs)
            for k, v in kwargs.items():
                setattr(view, k, v)
            return view

        return type(class_view.__name__, (class_view,), {'as_view': classonlymethod(as_view)})
    return wrapper


"""
def allow_all(func):
    def wrapper(class_view):
        def as_view(cls, **init_kwargs):
            view = super(cls, cls).as_view(**init_kwargs)
            view._allow_all_users = True
            return view

        return type(class_view.__name__, (class_view,), {'as_view': classonlymethod(as_view)})
    return wrapper
"""

def allow_all(func):
    func._allow_all_users = True

    def wrapper():
        func()

    return wrapper
