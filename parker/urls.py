from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'parker.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^parker/', include('empresa.urls')),
    url(r'^parker/', include('inventario.urls')),
    url(r'^parker/admin/', include(admin.site.urls)),
    url(r'^parker/matriculas/', include('matriculas.urls')),
]
