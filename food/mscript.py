from .models import Food, FoodInstance, Meal, Nutrient, NutrientInstance, NutrientCategory
import json
import django.db.utils


def create_nutrientcategory(name):
    if (NutrientCategory.objects.filter(category_name=name).exists()):
        print(name, "is already exist.")
    else:
        c = NutrientCategory(category_name=name)
        return c

def delete_nutrientcategory(name):
    if (not NutrientCategory.objects.filter(category_name=name).exists()):
        print(name, "doesn't exist.")
    else:
        NutrientCategory.objects.filter(category_name=name).delete()
        print(NutrientCategory.objects.all())

def create_nutrient(name):
    if (Nutrient.objects.filter(name=name).exists()):
        print(name, "is already exist.")
    else:
        c = Nutrient(name=name)
        return c

def delete_nutrient(name):
    if (name == '__all__') :
        Nutrient.objects.all().delete()
    elif (not Nutrient.objects.filter(name=name).exists()):
        print(name, "doesn't exist.")
    else:
        Nutrient.objects.filter(name=name).delete()
        print(Nutrient.objects.all())

def load_nutrients_from_file(path=''):
    if (path == ''):
        path = 'data/nutrients.json'
    f = open(path)
    data = json.load(f)
    for d in data:
        if (Nutrient.objects.all().filter(name=d['name']).exists()):
            print("%s is already exist." % d['name'])
        else:
            if (not NutrientCategory.objects.filter(category_name=d['type']).exists()):
                c = NutrientCategory(
                    category_name=d['type']
                )
                c.save()
            n = Nutrient(
                name=d['name'],
                rda =d['rda'],
                wiki=d['wiki'],
                required=d['required'],
                category=d['type'],
            )
            n.save()
        # print('name:', d['name'])
        # print('rda:', d['rda'])
        # print('wiki:', d['wiki'])
        # print('required:', d['required'])
        # print('type:', d['type'])
        # print()


def load_foods_from_file(path=''):
    if (path == ''):
        path = 'data/foods.json'

    mfile = open(path)
    data = json.load(mfile)
    for d in data:
        print('Loading %s...' % d['name'])
        if (Food.objects.all().filter(food_name=d['name']).exists()):
            print("%s is already exist." % d['name'])
        else:
            f = Food()
            f.food_name = d['name']
            f.fat = d['fat']
            f.calories = d['calories']
            f.proteins = d['proteins']
            f.carbohydrates = d['carbohydrates']
            f.serving = d['serving']
            f.save()
            for name in d['nutrients']:
                try:
                    n = Nutrient.objects.get(name=name)
                    nInstance = NutrientInstance()
                    nInstance.nutrient = n
                    nInstance.food = f
                    if (d['nutrients'][name] == None):
                        nInstance.amount = 0
                    else:
                        nInstance.amount = d['nutrients'][name]
                    nInstance.save()
                except django.db.utils.IntegrityError:
                    print(name + ' from ' + d['name'], "has an IntegrityError!")
                    print(d['nutrients'][name])


