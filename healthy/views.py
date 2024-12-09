from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *

#워드 클라우드 생성에 필요한 라이브러리 
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from konlpy.tag import Hannanum
from io import BytesIO
from collections import Counter
import numpy as np
from PIL import Image

# 제품 검색 페이지(본 페이지)
def search(reqeust):
    query = reqeust.GET.get('q', '') #검색어 가져오기 
    selected_product = ''
    print('입력단어:', query)
    if query:
        selected_product = product.objects.filter(product_name__contains=query) 
        print(selected_product)
    

    return render(reqeust, 'healthy/search_result.html', {'products': selected_product, 'query':query})



#제품 리뷰 보여주기 
def product_reviews(request, product_id):
    searched_product = get_object_or_404(product, pk=product_id)
    reviews = review.objects.filter(product_id=searched_product)
    return render(request, 'healthy/product_reviews.html', {'product': searched_product, 'reviews': reviews})



#제품 리뷰 - 워드 클라우드 보여주기
def product_reviews_wordcloud(request, product_id):
    hannanum = Hannanum()
    words = []

    # 해당 상품에 대한 리뷰 가져오기
    reviews = review.objects.filter(product_id=product_id)
    review_texts = [review.review_data for review in reviews]
    
    # 리뷰 데이터를 하나의 문자열로 합침
    text = ' '.join(review_texts)
    
    #자주 등장한 숫자 세기 
    nouns = hannanum.nouns(text)
    counter = Counter(nouns)
    
    #마스크 이미지
    cluoud_image = np.array(Image.open("C:/Users/ryeon/Documents/YerinShin/DevCourseDE/first_project/data/cloud.png"))

    # 워드 클라우드 생성
    wordcloud = WordCloud(font_path="C:/Users/ryeon/Documents/YerinShin/DevCourseDE/data crawling/week3-2/Paperlogy-4Regular.ttf", 
                        mask=cluoud_image,
                        width=800,
                        height=400,
                        background_color="white").generate(text)

    # 이미지를 메모리에 저장
    image = BytesIO()
    wordcloud.to_image().save(image, format='PNG')
    image.seek(0)

    # 이미지를 HTTP 응답으로 반환
    return HttpResponse(image, content_type='image/png')
    
    