# Generated by Django 3.0.3 on 2020-09-28 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0003_plant_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='standplace',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='watering',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='plant',
            name='age',
            field=models.DateTimeField(null=True),
        ),
    ]
