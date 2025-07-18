# Generated by Django 5.1.4 on 2024-12-26 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=10)),
                ('starting_date', models.DateField()),
                ('days', models.IntegerField()),
                ('people', models.IntegerField()),
                ('room', models.CharField(max_length=50)),
            ],
        ),
    ]
