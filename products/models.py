from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Product(models.Model):
    # 앞부분 F는 데이터 베이스 저장되는 문자, 뒤에 Fruit는 유저에게 보여지는 문자
    CATEGORY_CHOICES = ( 
        ("F", "Fruit"),
        ("V", "Vegetable"),
        ("M", "Meat"),
        ("O", "Other"),
    )

    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()  # PositiveIntegerField는 양수의 정수값
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
