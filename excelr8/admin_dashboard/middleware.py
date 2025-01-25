from django.shortcuts import redirect
from django.urls import reverse

class SuperUserOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '4dm1n_d4shb04rd_3987234098274091823712931' in request.path:
            if not request.user.is_authenticated or not request.user.is_superuser:
                return redirect('/4dm1n_d4shb04rd_142004/')
        

        return self.get_response(request)
