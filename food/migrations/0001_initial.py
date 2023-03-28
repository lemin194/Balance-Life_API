# Generated by Django 4.1.7 on 2023-03-28 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=30)),
                ('fat', models.DecimalField(decimal_places=2, default=100, max_digits=15)),
                ('calories', models.DecimalField(decimal_places=2, default=100, max_digits=15)),
                ('proteins', models.DecimalField(decimal_places=2, default=100, max_digits=15)),
                ('carbohydrates', models.DecimalField(decimal_places=2, default=100, max_digits=15)),
                ('serving', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Nutrient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nutrient_name', models.CharField(max_length=200)),
                ('rda', models.DecimalField(decimal_places=2, default=100, max_digits=15)),
                ('wiki', models.TextField()),
                ('required', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['nutrient_name'],
            },
        ),
        migrations.CreateModel(
            name='NutrientCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Nutrient Category',
                'verbose_name_plural': 'Nutrient Categories',
            },
        ),
        migrations.CreateModel(
            name='NutrientInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=100, max_digits=15)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.food')),
                ('nutrient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.nutrient')),
            ],
            options={
                'ordering': ['nutrient__nutrient_name'],
            },
        ),
        migrations.AddField(
            model_name='nutrient',
            name='_category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='food.nutrientcategory'),
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['time'],
            },
        ),
        migrations.CreateModel(
            name='FoodInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=100)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.food')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.meal')),
            ],
            options={
                'ordering': ['food__food_name'],
            },
        ),
    ]
