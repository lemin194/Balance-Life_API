from .models import Food, FoodInstance, Meal, Nutrient, NutrientInstance, NutrientCategory
import json

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)



def create_foodinstances_from_food_set(food_set, meal):
    for food in food_set:
        foodinstance=FoodInstance.objects.create(
            food=Food.objects.get(food_name=food['food_name']),
            meal=meal,
            amount=food['amount']
        )



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
    if (Nutrient.objects.filter(nutrient_name=name).exists()):
        print(name, "is already exist.")
    else:
        c = Nutrient(nutrient_name=name)
        return c

def delete_nutrient(name):
    if (name == '__all__') :
        Nutrient.objects.all().delete()
    elif (not Nutrient.objects.filter(nutrient_name=name).exists()):
        print(name, "doesn't exist.")
    else:
        Nutrient.objects.filter(nutrient_name=name).delete()
        print(Nutrient.objects.all())

def load_nutrients_from_file(path=''):
    if (path == ''):
        path = 'data/nutrients.json'
    f = open(path)
    data = json.load(f)
    response = ""
    for d in data:
        if (not Nutrient.objects.all().filter(nutrient_name=d['name']).exists()):
            if (not NutrientCategory.objects.filter(category_name=d['type']).exists()):
                c = NutrientCategory(
                    category_name=d['type']
                )
                c.save()
            n = Nutrient(
                nutrient_name=d['name'],
                rda =d['rda'],
                wiki=d['wiki'],
                required=d['required'],
                category=d['type'],
            )
            n.save()


def load_foods_from_file(path=''):
    if (path == ''):
        path = 'data/foods.json'

    mfile = open(path)
    data = json.load(mfile)
    for d in data:
        if (not Food.objects.all().filter(food_name=d['name']).exists()):
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
                    n = Nutrient.objects.get(nutrient_name=name)
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



def food_instance_list_to_json(filist):
    mlist = []
    for fi in filist:
        fidict = {}
        fidict['food_id'] = fi.food.id
        fidict['meal_id'] = fi.meal.id
        fidict['amount'] = fi.amount
        mlist.append(fidict)
    
    return json.dumps(mlist)

def food_list_to_json(flist):
    fdict = {}
    for f in flist:
        fdict[f.id] = f.food_name
    
    return json.dumps(fdict)


def json_to_food_instance_list(mjson):
    mlistjson = json.loads(mjson)
    filist = []
    for fidict in mlistjson:
        fi = FoodInstance()
        fi.food = Food.objects.get(id=fidict['food_id'])
        fi.meal = Meal.objects.get(id=fidict['meal_id'])
        fi.amount = fidict['amount']
        filist.append(f)
    return filist

    
def json_to_food_list(mjson):
    mdictjson = json.loads(mjson)
    flist = []
    for fid in mlistjson:
        f = Food().objects.get(id=fid)
        flist.append(f)
    return flist