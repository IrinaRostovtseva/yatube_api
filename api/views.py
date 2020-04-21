from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Comment, Follow, Group, Post
from .permissions import isAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [isAuthorOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwargs = ('post', 'id')
    permission_classes = [isAuthorOrReadOnly, ]

    def list(self, request, **kwargs):
        queryset = Comment.objects.filter(post=kwargs['post_id'])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        following = request.data.get('following')
        try:
            following_user = User.objects.get(username=following)
            is_follow = Follow.objects.filter(
                user=request.user, following=following_user).exists()
            if is_follow:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        if not following or following == request.user.username:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
