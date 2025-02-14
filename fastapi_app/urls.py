from django.contrib import admin
from django.http import JsonResponse
from django.urls import path


def django_main(request):
    return JsonResponse({"message": "Hello from Django!"})


urlpatterns = [
    path("", django_main, name="django_main"),
    path("admin/", admin.site.urls),
]
