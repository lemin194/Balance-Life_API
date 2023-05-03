from django.db import models
from django.contrib.auth.models import User


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    
    class Role(models.TextChoices):
        NORMAL = "Normal"
        SPECIALIST = "Specialist"
    role = models.CharField(max_length=50, choices=Role.choices, default="Normal")
    profile_image = models.ImageField(upload_to='images/profile_image/', default='images/profile_image/noavatar.png', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=30)
    fat = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    calories = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    proteins = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    carbohydrates = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    serving = models.IntegerField(default=100)
    def __str__(self):
        return self.ingredient_name

class Food(models.Model):
    food_name = models.CharField(max_length=30)
    food_description = models.CharField(max_length=255, default="")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/food/', null=True, blank=True)
    def __str__(self):
        return f"{self.food_name}"
        

class Meal(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    time = models.DateTimeField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['time']

    def __str__(self):
        return (self.title if (self.title != None) else '')\
        + ' ' + self.time.strftime('%Y-%m-%d %H:%M')



class Nutrient(models.Model) :
    nutrient_name = models.CharField(max_length=200)
    rda = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    wiki = models.TextField()
    required = models.BooleanField(default=True)
    category = models.CharField(max_length=200, null=True, blank=True)

    
    class Meta:
        ordering = ['nutrient_name']
        

    def __str__(self):
        return f'{self.nutrient_name}'



class NutrientInstance(models.Model):
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    
    class Meta:
        ordering = ['nutrient__nutrient_name']

    def __str__(self):
        return f'{self.nutrient.nutrient_name}'


class IngredientInstance(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['ingredient__ingredient_name']
        
    def __str__(self):
        return self.ingredient.ingredient_name

class FoodInstance(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.food.food_name}'