from django.http import JsonResponse
import time

class BlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            return JsonResponse({'error': 'account is inactive'}, status=403)
        return self.get_response(request)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if not user.is_authenticated:
           user = None  
        method = request.method
        path = request.path
        response = self.get_response(request)
        status = response.status_code

        print(f'{user} | {method} | {path} | status: {status}')
        return response
    
class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(request.path, 'in', duration, 'sec')
        return response