
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main.urls')),
    path('support/', include('support.urls')),
    path('', include('registros.urls')),
    path('', include('registrosgab.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('markdownx/', include('markdownx.urls')),
    path('', include('configapp.urls')),
    ]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        ]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
