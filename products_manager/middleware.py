from django.core.exceptions import PermissionDenied


class SuperuserRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/gerencia/"):
            if not request.user.is_authenticated or not request.user.is_superuser:
                raise PermissionDenied
        return self.get_response(request)
