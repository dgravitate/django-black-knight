from django.conf import settings
from django.shortcuts import redirect


class BlackKnightMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path == settings.LOGIN_URL:
            return None

        if hasattr(view_func, '_allow_all_users') and view_func._allow_all_users:
            return None

        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        # check permissions from dynamically generated decorators
