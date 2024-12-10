from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_page, name="main_page_make"),
    path("search/", views.search, name="search_results_make"),
    path("product/<int:product_id>/", views.product_reviews, name="product_reviews_make"),
    path("product/<int:product_id>/wordcloud/", views.product_reviews_wordcloud, name="product_reviews_wordcloud_make"),
]