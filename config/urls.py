from django.contrib import admin
from django.urls import include, path

from university import views


urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("subjects/", include("university.urls")),
]