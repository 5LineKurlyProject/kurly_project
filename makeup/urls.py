from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("search/", views.search, name="search_results"),
    path("product/<int:product_id>/", views.product_reviews, name="product_reviews"),
    path("product/<int:product_id>/wordcloud/", views.product_reviews_wordcloud, name="product_reviews_wordcloud"),
]