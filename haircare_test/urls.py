from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='haircare_test/main_page'),
    path("search", views.search, name='haircare_test/search'),
    path("product/<int:product_id>/", views.product_reviews, name='haircare_test/product_reviews'),
    path('product/<int:product_id>/wordcloud/', views.product_reviews_wordcloud, name='haircare_test/product_reviews_wordcloud'),
]