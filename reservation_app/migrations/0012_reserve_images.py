# Generated by Django 5.1.3 on 2025-01-02 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0011_alter_reserve_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='images',
            field=models.ManyToManyField(max_length=models.IntegerField(), related_name='image_set', to='reservation_app.image'),
        ),
    ]
