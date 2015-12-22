from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from common.views import TestEmail

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('inventario.urls')),
    url(r'^', include('tickets.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^test_email', TestEmail.as_view()),
]

urlpatterns = [
    url(r'^parker/', include(urlpatterns)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
