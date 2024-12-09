from django.core.management.base import BaseCommand
import pandas as pd
from luxury_beauty.models import Product, Category, Review


class Command(BaseCommand):
    help = "Import CSV data into Django database using ORM"

    def handle(self, *args, **options):
        # CSV 파일 경로
        csv_file_path = "data/luxury_data.csv"

        # CSV 데이터 읽기
        try:
            data = pd.read_csv(csv_file_path)
            self.stdout.write(f"Successfully read CSV file: {csv_file_path}")
        except FileNotFoundError:
            self.stderr.write(f"Error: File not found at {csv_file_path}")
            return

        # 카테고리 생성/조회
        category_name = "Luxury Beauty"
        category, created = Category.objects.get_or_create(category_name=category_name)

        # 데이터 삽입
        for _, row in data.iterrows():
            product_name = row['product_name']
            image_url = row['img_url']
            review_text = row['review']

            # Product 생성 또는 가져오기
            product, created = Product.objects.get_or_create(
                product_name=product_name,
                defaults={'image_url': image_url}
            )

            # Product와 Category 관계 설정
            product.categories.add(category)

            # Review 생성
            Review.objects.create(product=product, review=review_text)

        self.stdout.write(self.style.SUCCESS("CSV data imported successfully!"))
