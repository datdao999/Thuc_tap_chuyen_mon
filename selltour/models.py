from django.db import models
from django.shortcuts import reverse


# Create your models here.
class Customer(models.Model):
    id_Customer = models.AutoField(primary_key=True)
    name_Customer = models.CharField(max_length=256, null = True)
    email = models.CharField(max_length=256, null = True)
    phone_Number = models.CharField(max_length=256)

class Type_Tour(models.Model):
    id_Type = models.AutoField(primary_key=True)
    name_Type = models.CharField(max_length=256)

    def __str__(self):
        return self.name_Type

class Tour(models.Model):
    id_Tour = models.AutoField(primary_key=True)
    name_Tour = models.CharField(max_length= 256)
    price_Tour = models.IntegerField()
    date_Start = models.DateField()
    origin_Place = models.CharField(max_length=256)
    type_Tour = models.ForeignKey(Type_Tour, on_delete = models.CASCADE)
    image_Tour = models.ImageField(null=True, blank = True)
    last = models.IntegerField()
    detail = models.TextField(null = True, blank = True)
    slug = models.SlugField()

    

    def __str__(self):
        return self.name_Tour

    @property
    def imageURL(self):
        try:
            url_text = self.image_Tour.url
        except:
            url_text = ''
        return url_text

    def get_absolute_url(self):
        return reverse("selltour:detail", kwargs={
            'slug': self.slug
        })

    def get_information_order(self):
        return reverse("selltour:information_order", kwargs={
            'slug': self.slug
        })
    def get_information_guess(self):
        return reverse("selltour:information_guess", kwargs={
            'slug': self.slug
        })


class Image_of_Tour(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    image_Tour = models.ImageField(null = True, blank = True)

class Order_Tour (models.Model):
    tour = models.ForeignKey(Tour, on_delete= models.CASCADE )
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    Date_Order = models.DateField(auto_now_add=True)
    Quantity = models.IntegerField()
    Toal_Money = models.IntegerField()

class Information_Guess(models.Model):
    id_Guess = models.AutoField(primary_key= True)
    tour = models.ForeignKey(Tour, on_delete= models.CASCADE )
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    name_Guess = models.CharField(max_length=256)
    sex = models.BooleanField(default=False)
    birthday = models.DateField()
    
class News (models.Model):
    id_News = models.AutoField(primary_key=True)
    titlle = models.CharField(max_length=256)
    content = models.TextField()

class Image_of_News(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    image = models.ImageField(null = True, blank = True)

class Country (models.Model):
    id_Country = models.AutoField(primary_key=True)
    name_Country = models.CharField(max_length=256)

    def __str__(self):
        return self.name_Country

class City (models.Model):
    id_City = models.AutoField(primary_key=True)
    name_City = models.CharField(max_length=256)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_City

class User(models.Model):
    id_User = models.AutoField(primary_key=True)
    name_User = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    permission = models.IntegerField()

class Through (models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    class Meta ():
        unique_together = ['tour', 'city']

    