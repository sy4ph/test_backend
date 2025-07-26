from django.urls import path
from . import views

app_name = 'tree_menu'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin_redirect, name='admin_redirect'),
    path('<path:page_path>/', views.dynamic_page, name='dynamic_page'),
]
