import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from allauth.account.views import confirm_email
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view, SwaggerUIRenderer
from drf_yasg import openapi

SwaggerUIRenderer.template = 'drf-yasg.html'


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=True):
        schema = super(SchemaGenerator, self).get_schema(request, public)
        schema.basePath = os.path.join(schema.basePath, '')
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Football Opinionated API",
        default_version='v1',
        description="the api service for footbllopinionated.com, a web app for discussing soccer related issues.",
        ),
    public=True,
    url='https://footballopinionated.com/',
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("home/", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("football_opinionated.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', confirm_email, name='account_confirm_email'),
    # Docs
    path('api/v1/documentation/', schema_view.as_view(), {'format': '.json'}, name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Your stuff: custom urls includes go here
    path("api/questions/", include("Questions.api.urls", namespace="questions-api")),
    path("api/comments/", include("Comment.api.urls", namespace="comment-api")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
