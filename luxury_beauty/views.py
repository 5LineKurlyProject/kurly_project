from django.shortcuts import render, get_object_or_404
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Hannanum
import pandas as pd
from PIL import Image
import numpy as np
import requests
from io import BytesIO
import base64
import tkinter
import os
from django.conf import settings
from healthy.models import Product, Category, Review

# CSV 파일 경로
csv_path = 'data/kurly_test_5.csv'

# 형태소 분석기 및 폰트 경로
hannanum = Hannanum()
korean_font_path = "C:/Users/ekfrl/AppData/Local/Microsoft/Windows/Fonts/HakgyoansimSonagiR.ttf"

def index(request):
    # 카테고리 직접 정의
    # categories = ['luxury_beauty', '메이크업', '스킨케어', '헤어케어', '건강식품']
    categories = Category.objects.all()
    print("categories: ")
    for category in categories:
        print(category.category_name)

    return render(request, 'luxury_beauty/index.html', {'categories': categories})

def product_reviews(request, category):
    print(f"category: {category}")
    
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    # 형태소 분석기
    hannanum = Hannanum()

    # 마스킹 이미지
    # mask_image_path = "C:/Users/ekfrl/Dev_course_5/masking_image.jpg"
    mask_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'lip.jpg')
    mask_image = Image.open(mask_image_path)
    mask_array = np.array(mask_image)

    # 상품별 시각화
    products = []
    for product_name in df['상품 이름'].unique():
        # 해당 상품의 리뷰와 이미지 URL 추출
        product_reviews = df[df['상품 이름'] == product_name]['리뷰'].tolist()
        product_image_url = df[df['상품 이름'] == product_name]['이미지 url'].iloc[0]

        # 이미지 불러오기
        try:
            response = requests.get(product_image_url)
            product_image = Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"이미지 불러오기 실패 ({product_name}): {e}")
            continue

        # print(product_name)
        # print(product_reviews)
        
        # 형태소 분석 및 단어 빈도 계산
        words = []
        for review in product_reviews:
            nouns = hannanum.nouns(review)
            words += nouns
        counter = Counter(words)

        # 워드클라우드 생성
        wordcloud = WordCloud(
            font_path=korean_font_path,
            background_color="white",
            # max_words=10,
            mask=mask_array,
            width=1000,
            height=1000
        ).generate_from_frequencies(counter)

        # 워드클라우드 이미지 저장
        buffer = BytesIO()
        plt.figure(figsize=(5, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis('off')
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        wordcloud_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        
        # 상품 이미지 저장
        buffer = BytesIO()
        product_image.save(buffer, format='PNG')
        product_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        
        # 결과 저장
        products.append({
            'name': product_name,
            'reviews': product_reviews,
            'wordcloud': wordcloud_base64,
            'image': product_image_base64
        })

    return render(request, 'luxury_beauty/product_reviews.html', {'products': products, 'category':category})

def search_result(request):
    category = request.GET.get('category', '기본 카테고리')
    query = request.GET.get('query', '')
    
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    # 검색어를 포함한 데이터 필터링
    filtered_df = df[df['상품 이름'].str.contains(query, na=False)]
    if filtered_df.empty:
        return render(request, 'luxury_beauty/product_search.html', {
            'error': f'"{query}"에 해당하는 상품이 없습니다.',
            'query': query
        })
        
    # 마스킹 이미지
    # mask_image_path = "C:/Users/ekfrl/Dev_course_5/masking_image.jpg"
    mask_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'lip.jpg')
    mask_image = Image.open(mask_image_path)
    mask_array = np.array(mask_image)
    
    products = []
    
    # 중복 제거를 위해 상품 이름 기준으로 그룹화
    grouped = filtered_df.groupby('상품 이름')
    for product_name, group in grouped:
        product_reviews = group['리뷰'].tolist()
        product_image_url = group['이미지 url'].iloc[0]  # 첫 번째 URL 사용
        
        # 상품 이미지 가져오기
        try:
            response = requests.get(product_image_url)
            product_image = Image.open(BytesIO(response.content))
            buffer = BytesIO()
            product_image.save(buffer, format='PNG')
            product_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
        except Exception as e:
            print(f"이미지 불러오기 실패 ({product_name}): {e}")
            product_image_base64 = None
            
        # 리뷰 수집 및 형태소 분석
        words = []
        for review in product_reviews:
            nouns = hannanum.nouns(review)
            words += nouns
        counter = Counter(words)

        # 워드클라우드 생성
        wordcloud = WordCloud(
            font_path=korean_font_path,
            background_color="white",
            mask=mask_array,
            width=1000,
            height=1000
        ).generate_from_frequencies(counter)
        
        # 워드클라우드 이미지 저장
        buffer = BytesIO()
        plt.figure(figsize=(5, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        wordcloud_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        
        # 상품 데이터 저장
        products.append({
            'name': product_name,
            'image': product_image_base64,
            'wordcloud': wordcloud_base64
        })

    return render(request, 'luxury_beauty/search_result.html', {
        'query': query,
        'products': products,
        'category': category,
    })