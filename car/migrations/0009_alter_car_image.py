# Generated by Django 4.1.7 on 2023-03-31 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0008_alter_bid_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.TextField(),
        ),
    ]
