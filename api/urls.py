from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comment')
router.register(r'group', GroupViewSet, basename='group')
router.register(r'follow', FollowViewSet, basename='follow')


urlpatterns = [
    path('', include(router.urls)),
]
