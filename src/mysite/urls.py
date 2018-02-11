from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^tags_input/', include('tags_input.urls', namespace='tags_input')),
    url(r'^admin/', admin.site.urls),
    url(r'',include('webapp.urls')),
]
