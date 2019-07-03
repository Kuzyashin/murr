from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Murren import views as murren
from .views import redirect_view, about
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Murrengan API')


urlpatterns = [
    path('', redirect_view, name='redirect_view'),
    path('admin/', admin.site.urls),
    path('about/', about, name='about'),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('edit/', murren.murren_edit, name='edit'),
    path('murrs/', include('MurrCard.urls')),
    path('landing/', murren.landing, name='landing'),
    path('murren/', include('Murren.urls')),
    path('dashboard/', include('Dashboard.urls')),
    url(r'^docs/$', schema_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
