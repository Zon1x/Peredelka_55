from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_list, name='portfolio_list'),
    path('category/<slug:category_slug>/', views.portfolio_list, name='portfolio_list_by_category'),
    path('<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
]
