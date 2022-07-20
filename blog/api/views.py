from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from blango_auth.models import User
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer, TagSerializer
from blog.models import Post, Tag


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return PostSerializer
        else:
            return PostDetailSerializer


class UserDetail(generics.RetrieveAPIView):
    lookup_field = 'email'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(methods=['get'], detail=True, name='Posts with the tag')
    def posts(self, request, pk=None):
        tag = self.get_object()
        post_serializer = PostSerializer(tag.posts, many=True, context={'request': request})
        return Response(post_serializer.data)

