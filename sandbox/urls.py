from django.contrib import admin
from django.urls import path
from sandbox import views as sandbox_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth', sandbox_views.AuthAPI.as_view()),
    path('api/user-list', sandbox_views.UsersAPI.as_view()),
]
