# Generated by Django 5.0.3 on 2024-03-19 03:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("links", "0005_alter_favlink_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="favlink",
            name="title",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=50),
        ),
    ]
