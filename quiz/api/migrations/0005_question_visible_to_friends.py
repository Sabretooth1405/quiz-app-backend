# Generated by Django 4.1.7 on 2023-03-19 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_friendshiprequests_friendship"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="visible_to_friends",
            field=models.BooleanField(default=False),
        ),
    ]