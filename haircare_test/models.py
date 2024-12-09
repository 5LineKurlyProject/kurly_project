from django.db import models

# Category 테이블
class hair_Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)  # 카테고리명

    def __str__(self):
        return self.category_name


# Product 테이블
class hair_Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)  # 상품 이름
    image_url = models.URLField(blank=True, null=True)  # 이미지 URL
    categories = models.ManyToManyField(hair_Category, related_name='products')  # 다대다 관계

    def __str__(self):
        return self.product_name


# Review 테이블
class hair_Review(models.Model):
    product = models.ForeignKey(hair_Product, on_delete=models.CASCADE)  # 리뷰가 속한 제품
    review = models.TextField()  # 리뷰 내용

    def __str__(self):
        return f"{self.product.product_name}: {self.review[:20]}..."  # 리뷰 내용 일부 표시