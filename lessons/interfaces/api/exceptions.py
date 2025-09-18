import logging

from django.http import JsonResponse
from lessons.domain.exceptions import ValidationError


class DomainExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ValidationError):
            logging.error("Domain validation error caught in middleware")
            return JsonResponse({"message": exception.message}, status=400)
        return None
