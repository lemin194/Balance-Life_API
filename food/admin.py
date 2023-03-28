from django.contrib import admin
from .models import Meal, Food, Nutrient, NutrientCategory, NutrientInstance, FoodInstance

# Register your models here.

class NutrientInstanceInline(admin.TabularInline):
    model = NutrientInstance
    extra = 1
class NutrientInline(admin.TabularInline):
    model = Nutrient
    extra = 1
class FoodInstanceInline(admin.TabularInline):
    model = FoodInstance
    extra = 1


class NutrientAdmin(admin.ModelAdmin):
    list_display = ('nutrient_name', 'rda', 'required', 'category')
    search_fields = ['nutrient_name', 'category']
    list_filter = ['_category__category_name']

class NutrientCategoryAdmin(admin.ModelAdmin):
    inlines = [NutrientInline]
    search_fields = ['category_name']

class FoodAdmin(admin.ModelAdmin):
    inlines = [NutrientInstanceInline]
    list_display = ('food_name', 'calories', 'proteins', 'fat', 'carbohydrates')
    search_fields = ['nutrient_name']
    list_filter = ['food_name', 'calories', 'proteins', 'fat', 'carbohydrates']

class MealAdmin(admin.ModelAdmin):
    inlines = [FoodInstanceInline]
    list_display = ('title', 'time')
    search_fields = ['title', 'time']




admin.site.register(Food, FoodAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Nutrient, NutrientAdmin)
admin.site.register(NutrientCategory, NutrientCategoryAdmin)