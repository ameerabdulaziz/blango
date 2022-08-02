from datetime import timedelta

from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from blango_auth.models import User
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer, TagSerializer
from blog.models import Post, Tag


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if not user.is_staff:
                self.queryset = self.queryset.filter(Q(published_at__lt=timezone.now()) | Q(author=user))
        else:
            self.queryset = self.queryset.filter(published_at__lt=timezone.now())
        period_time = self.kwargs.get('period_time')
        if not period_time:
            return self.queryset
        else:
            if period_time == 'new':
                return self.queryset.filter(published_at__gt=timezone.now() - timedelta(hours=1))
            elif period_time == 'day':
                return self.queryset.filter(published_at__gt=timezone.now() - timedelta(days=1))
            elif period_time == 'week':
                return self.queryset.filter(published_at__gt=timezone.now() - timedelta(weeks=1))
            else:
                raise Http404(f"Time period {period_time} is not valid, should be 'new', 'today' or 'week'")

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return PostSerializer
        else:
            return PostDetailSerializer

    @method_decorator(cache_page(120))
    @method_decorator(vary_on_headers('Authorization', 'Cookie'))
    def list(self, *args, **kwargs):
        return super(PostViewSet, self).list(*args, **kwargs)
    
    @method_decorator(cache_page(300))
    @method_decorator(vary_on_headers('Authorization', 'cookie'))
    @action(methods=['get'], detail=False, name='Posts by the logged in user')
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Posts are yours")
        posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class UserDetail(generics.RetrieveAPIView):
    lookup_field = 'email'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @method_decorator(cache_page(300))
    def get(self, *args, **kwargs):
        return super(UserDetail, self).get(*args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    @method_decorator(cache_page(300))
    def list(self, request, *args, **kwargs):
        return super(TagViewSet, self).list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super(TagViewSet, self).retrieve(request, *args, **kwargs)
    
    @action(methods=['get'], detail=True, name='Posts with the tag')
    def posts(self, request, pk=None):
        tag = self.get_object()
        post_serializer = PostSerializer(tag.posts, many=True, context={'request': request})
        return Response(post_serializer.data)

