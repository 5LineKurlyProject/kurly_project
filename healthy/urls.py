from django.urls import path
from healthy import views

urlpatterns = [
    
    #루트 경로로 들어왔을 경우, 검색 페이지를 보여줌 
    path("", views.main_page, name='healthy/main_page'),
    path("search", views.search, name='healthy/search'),
    path("product/<int:product_id>/", views.product_reviews, name='healthy/product_reviews'),
    path('product/<int:product_id>/wordcloud/', views.product_reviews_wordcloud, name='healthy/product_reviews_wordcloud'),
]