# Generated by Django 4.1.2 on 2022-10-26 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date_added',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='blog',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
