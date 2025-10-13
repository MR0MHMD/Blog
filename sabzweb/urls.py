from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from Blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('Blog.urls', namespace='blog')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)












