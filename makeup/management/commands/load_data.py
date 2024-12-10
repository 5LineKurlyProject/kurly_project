import csv
from django.core.management.base import BaseCommand
from makeup.models import product, review  # 모델 임포트


class Command(BaseCommand):
    help = 'Load data from CSV'

    def handle(self, *args, **kwargs):
        file_path = "/Users/gimgyeong-yeong/Programmers/webcrawl/processed_product_data.csv"
        
        with open(file_path, encoding="utf-8-sig") as file:  # utf-8-sig로 BOM 처리
            reader = csv.DictReader(file)
            print(f"CSV 헤더: {reader.fieldnames}")  # 헤더 확인
            
            for row in reader:
                product_name = row['상품 이름']
                image_url = row['이미지 URL']
                review_data = row['리뷰']
                
                # Product 생성 또는 가져오기
                product_obj, created = product.objects.get_or_create(
                    product_name=product_name,
                    defaults={'image_url': image_url}
                )
                
                # Review 추가
                review.objects.create(
                    product_id=product_obj,
                    review_data=review_data
                )
        
        self.stdout.write(self.style.SUCCESS("CSV 데이터가 성공적으로 로드되었습니다."))