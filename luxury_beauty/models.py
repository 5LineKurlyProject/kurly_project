# from django.db import models


# # Product 테이블
# class Product(models.Model):
#     product_name = models.CharField(max_length=255, unique=True)  # 상품 이름
#     image_url = models.URLField(blank=True, null=True)  # 이미지 URL
#     categories = models.ManyToManyField(Category, related_name='products')  # 다대다 관계

#     def __str__(self):
#         return self.product_name


# # Category 테이블
# class Category(models.Model):
#     category_name = models.CharField(max_length=255, unique=True)  # 카테고리명

#     def __str__(self):
#         return self.category_name


# # ProductCategory 테이블 (다대다 관계 테이블)
# class ProductCategory(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.product.product_name} - {self.category.category_name}"


# # Review 테이블
# class Review(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 리뷰가 속한 제품
#     review_data = models.TextField()  # 리뷰 내용

#     def __str__(self):
#         return f"{self.product.product_name}: {self.review_data[:20]}..."  # 리뷰 내용 일부 표시