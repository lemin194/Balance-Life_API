# Generated by Django 4.1.7 on 2023-05-03 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_food_food_description_food_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='food_description',
            field=models.CharField(default='', max_length=255),
        ),
    ]
