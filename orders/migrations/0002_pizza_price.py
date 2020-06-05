# Generated by Django 3.0.6 on 2020-06-02 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=4),
        ),
    ]
