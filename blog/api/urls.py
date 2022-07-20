from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from blog.api.views import UserDetail, TagViewSet, PostViewSet

urlpatterns = [
    path("users/<str:email>/", UserDetail.as_view(), name="api_user_detail"),
]

schema_view = get_schema_view(
    openapi.Info(title="Blango API", default_version="v1", description="API for Blango Blog"),
    url="http://127.0.0.1:8000/api/v1/",
    public=True,
)


urlpatterns += [
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", views.obtain_auth_token),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('posts', PostViewSet)

urlpatterns += [
    path('', include(router.urls)),
]
