# Generated by Django 5.0.3 on 2024-03-19 09:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("links", "0007_favlink_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="favlink",
            name="note",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
