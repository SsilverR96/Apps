# Generated by Django 4.0.4 on 2022-05-15 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_site_htmlcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site',
            old_name='url',
            new_name='name',
        ),
    ]
