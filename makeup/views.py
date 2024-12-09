from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import product, review
from konlpy.tag import Hannanum
from collections import Counter
from wordcloud import WordCloud
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import os
from django.conf import settings

# 비GUI 백엔드 설정
matplotlib.use('Agg')

# 메인 페이지
def main_page(request):
    top_products = product.objects.all()[:6]  # 예시: 상위 6개 추천 상품
    return render(request, 'makeup/main_page.html', {'top_products': top_products})

# 검색 페이지
def search(request):
    query = request.GET.get('q', '')  # 검색어 가져오기
    selected_products = []

    if query:
        selected_products = product.objects.filter(product_name__icontains=query)  # 대소문자 구분 없이 검색

    return render(request, 'makeup/search_result.html', {'products': selected_products, 'query': query})

# 제품 리뷰 보기
def product_reviews(request, product_id):
    searched_product = get_object_or_404(product, pk=product_id)
    reviews = review.objects.filter(product_id=searched_product)
    return render(request, 'makeup/product_reviews.html', {'product': searched_product, 'reviews': reviews})

# 워드 클라우드 생성 및 보여주기
def product_reviews_wordcloud(request, product_id):
    hannanum = Hannanum()

    try:
        # 해당 상품에 대한 리뷰 가져오기
        reviews = review.objects.filter(product_id=product_id)
        review_texts = [review.review_data for review in reviews]

        # 리뷰가 없는 경우 처리
        if not review_texts:
            return HttpResponse("리뷰가 없습니다.", content_type="text/plain")

        # 리뷰 데이터를 하나의 문자열로 합침
        text = ' '.join(review_texts)

        # 명사 추출 및 빈도 계산
        nouns = hannanum.nouns(text)
        counter = Counter(nouns)

        # 워드 클라우드 생성
        wordcloud = WordCloud(
            font_path="/Library/Fonts/AppleGothic.ttf",  # MacOS용 기본 폰트 경로 (환경에 맞게 설정)
            background_color="white",
            width=800,
            height=400
        ).generate_from_frequencies(counter)

        # 워드 클라우드를 matplotlib로 렌더링 (웹 출력용)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")  # 축 제거

        # 워드 클라우드를 메모리에 저장
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format='png', bbox_inches='tight')
        plt.close()
        image_buffer.seek(0)

        return HttpResponse(image_buffer, content_type="image/png")

    except Exception as e:
        return HttpResponse(f"오류 발생: {str(e)}", content_type="text/plain")