from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>', views.archive),
    path('categories/<int:pk>', views.category),
    path('tags/<int:pk>', views.tag),
]