# Generated by Django 4.2.16 on 2024-11-09 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aqt', '0007_alter_role_roleid_alter_user_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='RoleID',
        ),
    ]