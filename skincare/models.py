from django.db import models

# Create your models here.

class product_contents(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=255, unique=True)
    image_url = models.TextField()
    

class review_contents(models.Model):
    review_id = models.IntegerField(primary_key=True)
    product_id = models.ForeignKey(product_contents, on_delete=models.CASCADE)
    review_data = models.TextField()
    
    
# Create your models here.
