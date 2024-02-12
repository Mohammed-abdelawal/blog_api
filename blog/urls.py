from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'api/',
        include('core.urls')
    ),
    path(
        'api/token/',
        obtain_auth_token,
        name='obtain-token'
    ),
    path(
        "ckeditor5/",
        include('django_ckeditor_5.urls'),
        name="ck_editor_5_upload_file"
    ),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
