from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:category>/', views.product_reviews, name='product_reviews'),
    path('search/', views.search_result, name='search_result'),
]