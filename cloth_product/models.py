from django.db import models
from django.contrib.auth.models import User
from cloth_category.models import Category

from .constraints import SIZE,STAR_CHOICES

class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='cloth_product/media/images')
    price = models.DecimalField(decimal_places=2,max_digits=10)
    quantity = models.IntegerField()
    description = models.TextField()
    size = models.CharField(max_length=100,null=True,blank=True,choices=SIZE)
    
    

    
    def __str__(self) -> str:
        return f" Product : {self.name} , Category: {self.category.name}"

class Wishlist (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,blank=True)

    # def __str__(self) -> str:
    #     return f"{self.user.usfirst_name}{self.user.last_name} {self.product.name} "




class Review(models.Model):
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10)
    
    # def __str__(self):
    #     return f"Reviewer: {self.reviewer.first_name} {self.reviewer.last_name} "