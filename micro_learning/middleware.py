class AllowAllHostsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META.get("HTTP_HOST")
        if not host:
            request.META["HTTP_HOST"] = 'micro-learning-backend-production.up.railway.app'
        return self.get_response(request)