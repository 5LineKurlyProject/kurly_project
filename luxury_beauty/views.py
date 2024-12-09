from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from luxury_beauty.models import Product, Category, Review
from django.conf import settings
import os

#워드 클라우드 생성에 필요한 라이브러리 
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Hannanum
from PIL import Image
import numpy as np
from io import BytesIO


def main_page(request):
    top_products = Product.objects.all().order_by('id')[:4]
    return render(request, 'luxury_beauty/main_page.html', {'top_products': top_products})

def product_reviews(request, product_id):
    searched_product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product_id=searched_product)
    return render(request, 'luxury_beauty/product_reviews.html', {'product': searched_product, 'reviews': reviews})

def product_reviews_wordcloud(request, product_id):
    
    # 해당 상품에 대한 리뷰 가져오기
    reviews = Review.objects.filter(product_id=product_id)
    review_texts = [review.review for review in reviews]
    
    # 리뷰 데이터를 하나의 문자열로 합침
    text = ' '.join(review_texts)
    
    # 형태소 분석기
    hannanum = Hannanum()
    
    #자주 등장한 숫자 세기 
    nouns = hannanum.nouns(text)
    counter = Counter(nouns)
    
    #마스크 이미지
    mask_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'lip.jpg')
    mask_image = Image.open(mask_image_path)
    mask_array = np.array(mask_image)
    
    # 폰트 경로
    font_path = os.path.join(settings.BASE_DIR, 'static', 'font', 'HakgyoansimSonagiR.ttf')
    
    # 워드클라우드 생성
    wordcloud = WordCloud(
        font_path=font_path,
        background_color="white",
        mask=mask_array,
        width=1000,
        height=1000).generate_from_frequencies(counter)

    # 이미지를 메모리에 저장
    image = BytesIO()
    wordcloud.to_image().save(image, format='PNG')
    image.seek(0)
    
    # 이미지를 HTTP 응답으로 반환
    return HttpResponse(image, content_type='image/png')

def search(request):
    query = request.GET.get('q', '')
    selected_product = ''
    if query:
        selected_product = Product.objects.filter(product_name__contains=query) 
        
    return render(request, 'luxury_beauty/search_result.html', {'products': selected_product, 'query':query})