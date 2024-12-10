#csv 파일 데이터 -> 테이블로 넣기 
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kurly_project.settings")

import django
django.setup()

import pandas as pd 
import csv
from healthy.models import product, review

PRODUCT_PATH = "C:/Users/ryeon/Documents/YerinShin/DevCourseDE/first_project/data/뷰티컬리_건강식품_product.csv"
REVIEW_PATH = "C:/Users/ryeon/Documents/YerinShin/DevCourseDE/first_project/data/뷰티컬리_건강식품_reviw.csv"


df1 = pd.read_csv(PRODUCT_PATH)

print(df1.columns)
    
for _, row in df1.iterrows():
    product_obj, created = product.objects.get_or_create(
        product_id = row['product_id'],
        defaults={
            "product_name": row["product_name"],
            "image_url": row['url']
        }
    )


df2 = pd.read_csv(REVIEW_PATH)
for _, row in df2.iterrows():
    review_obj, created = review.objects.get_or_create(
        review_id = row['review_id'],
        defaults={
            "product_id": product.objects.get(product_id=row["product_id"]),
            "review_data": row["review"],
        }
    )
    



