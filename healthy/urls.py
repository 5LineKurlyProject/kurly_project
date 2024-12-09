from django.urls import path
from . import views

urlpatterns = [
    
    #루트 경로로 들어왔을 경우, 검색 페이지를 보여줌 
    path("", views.main_page, name='main_page'),
    path("search", views.search, name='search'),
    path("product/<int:product_id>/", views.product_reviews, name='product_reviews'),
    path('product/<int:product_id>/wordcloud/', views.product_reviews_wordcloud, name='product_reviews_wordcloud'),
]