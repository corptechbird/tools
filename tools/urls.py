from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app'

urlpatterns = [
    path('', views.visualizer_index, name='visualizer_index'),
    path('cross/', views.cross_index, name='cross_index'),
    path('pivot/', views.cross_index, name='pivot_index'),
    path('export/', views.post_export, name='export')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
