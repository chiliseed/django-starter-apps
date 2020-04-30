from django.urls import include, path

from api import views

app_name = "api"
urlpatterns = [
    path("health/check", include('health_check.urls'), name="health_check"),
    path("hello/world", views.HelloWorld.as_view(), name="hello_world"),
]
