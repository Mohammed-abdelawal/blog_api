from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register('topics', views.TopicViewSet)
router.register('posts', views.PostViewSet)
router.register('authors', views.AuthorViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
]
