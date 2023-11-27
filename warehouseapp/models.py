from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.
class CustomUser(AbstractUser):
   
    user_type = models.CharField(default=1, max_length=10)
    
class Client(models.Model):
   
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True) 
    age=models.IntegerField()
    number=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    photo=models.FileField(upload_to='image/',null=True)
    
  
    
class Delivery(models.Model): 
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True) 
    number=models.CharField(max_length=255)
    image=models.ImageField(upload_to='image/',null=True,blank=True)
    
class Delivery1(models.Model): 
    user_type=models.CharField(default=2, max_length=10)
    number=models.CharField(max_length=255,null=True) 
    image=models.ImageField(upload_to='image/',null=True,blank=True)
    first_name=models.CharField(max_length=255,null=True)
    last_name=models.CharField(max_length=255,null=True)
    username=models.CharField(max_length=255,null=True) 
    email=models.EmailField(null=True)
    delivery=models.BooleanField(default=False)
    client=models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False) 
    
class Notification (models.Model):
    sender=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    message=models.TextField()
    is_read = models.BooleanField(default=False)
    

class Product(models.Model):
    name=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=40)
    qty = models.PositiveIntegerField(null=True)
    def __str__(self):
        return self.name


class Orders(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    client=models.ForeignKey('Client', on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True) 
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    
    
class AddressForm(models.Model):
    Email = models.EmailField(null=True)
    Mobile= models.IntegerField(null=True)
    Address = models.CharField(max_length=255,null=True) 
    Delivery_method=models.CharField(max_length=255,null=True)