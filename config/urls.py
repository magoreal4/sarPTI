
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from main.admin import admin_site 

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('admin/', admin_site.urls),
    path('', include('main.urls')),
    path('', include('registros.urls')),
    path('', include('registrosgab.urls')),
    ]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        ]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
