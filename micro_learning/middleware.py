class AllowAllHostsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.META.get("HTTP_HOST"):
            request.META["HTTP_HOST"] = "micro-learning-backend-production.up.railway.app"
        return self.get_response(request)
