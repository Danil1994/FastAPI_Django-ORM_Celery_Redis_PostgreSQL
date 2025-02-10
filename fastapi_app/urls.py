from django.urls import path
from django.http import JsonResponse


def django_main(request):
    return JsonResponse({"message": "Hello from Django!"})


urlpatterns = [
    path("", django_main, name="django_main"),
]
