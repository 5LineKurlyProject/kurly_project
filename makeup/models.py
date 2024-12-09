from django.db import models

class product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    image_url = models.TextField()

    def __str__(self):
        return self.product_name


class review(models.Model):
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    review_data = models.TextField()

    def __str__(self):
        return f"Review for {self.product_id.product_name}"