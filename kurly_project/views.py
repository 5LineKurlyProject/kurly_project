from django.http import HttpResponse
from django.shortcuts import render
from luxury_beauty.models import Product as LuxuryProduct
from healthy.models import product as HealthProduct
from skincare.models import product_contents as SkincareProduct
from makeup.models import product as MakeupProduct
from haircare_test.models import hair_Product


# 메인 페이지 뷰
def main_page(request):
    luxury_product = LuxuryProduct.objects.first()
    skincare_product = SkincareProduct.objects.first()
    health_product = HealthProduct.objects.first()
    makeup_product = MakeupProduct.objects.first()
    haircare_product = hair_Product.objects.first()
    
    img_url = {'luxury':luxury_product.image_url, 'skin':skincare_product.image_url, 'health':health_product.image_url, 'makeup':makeup_product.image_url, 'hair':haircare_product.image_url}
    
    return render(request, 'main.html', {'img_url': img_url})  # 템플릿 렌더링