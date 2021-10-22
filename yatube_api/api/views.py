from rest_framework import viewsets, filters
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Comment, User, Follow
from .serializers import PostSerializer, GroupSerializer, CommentSerializer, \
    FollowSerializer
from .permissions import UserIsAuthor

from rest_framework.pagination import LimitOffsetPagination


class PostViewSet(viewsets.ModelViewSet):
    """Все доступные методы."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, UserIsAuthor)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    """Все доступные методы."""
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, UserIsAuthor)

    def _get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        post_id = self._get_post().id
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        post = self._get_post()
        serializer.save(post=post, author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Только метод Get."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, UserIsAuthor)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def _get_user(self):
        return get_object_or_404(User, username=self.request.user)

    def get_queryset(self):
        user = self._get_user()
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
