# Generated by Django 3.1 on 2020-08-30 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20200830_1502'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='user',
            new_name='username',
        ),
    ]
