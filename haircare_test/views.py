from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from haircare_test.models import hair_Product, hair_Category, hair_Review
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
    top_products = hair_Product.objects.all().order_by('id')[:4]
    return render(request, 'haircare_test/main_page.html', {'top_products': top_products})

def product_reviews(request, product_id):
    searched_product = get_object_or_404(hair_Product, pk=product_id)
    reviews = hair_Review.objects.filter(product_id=searched_product)
    return render(request, 'haircare_test/product_reviews.html', {'product': searched_product, 'reviews': reviews})

import os
from collections import Counter
from django.http import HttpResponse
from django.conf import settings
from konlpy.tag import Hannanum
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from io import BytesIO
from .models import hair_Review

def product_reviews_wordcloud(request, product_id):
    try:
        # 해당 상품에 대한 리뷰 가져오기
        reviews = hair_Review.objects.filter(product_id=product_id)
        if not reviews.exists():
            return HttpResponse("No reviews found for this product.", status=404)
        print(reviews)
        review_texts = [review.review for review in reviews]
        text = ' '.join(review_texts).strip()

        if not text:
            return HttpResponse("No review text available to generate a word cloud.", status=404)

        # 형태소 분석기
        hannanum = Hannanum()
        nouns = hannanum.nouns(text)
        print(nouns)
        if not nouns:
            return HttpResponse("No valid words found to generate a word cloud.", status=404)

        # 단어 빈도수 계산
        counter = Counter(nouns)

        # 마스크 이미지 확인
        mask_image_path = os.path.join(settings.BASE_DIR, 'statics', 'images', 'cloud.png')
        if not os.path.exists(mask_image_path):
            return HttpResponse("Mask image not found.", status=500)

        mask_image = Image.open(mask_image_path)
        mask_array = np.array(mask_image)

        # 폰트 파일 확인
        font_path = os.path.join(settings.BASE_DIR, 'statics', 'fonts', 'Paperlogy-4Regular.ttf')
        if not os.path.exists(font_path):
            return HttpResponse("Font file not found.", status=500)

        # 워드클라우드 생성
        wordcloud = WordCloud(
            font_path=font_path,
            background_color="white",
            mask=mask_array,
            width=1000,
            height=1000
        ).generate_from_frequencies(counter)

        # 이미지를 메모리에 저장
        image = BytesIO()
        wordcloud.to_image().save(image, format='PNG')
        image.seek(0)

        return HttpResponse(image, content_type='image/png')

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def search(request):
    query = request.GET.get('q', '')
    selected_product = ''
    if query:
        selected_product = hair_Product.objects.filter(product_name__contains=query) 
        
    return render(request, 'haircare_test/search_result.html', {'products': selected_product, 'query':query})