# Generated by Django 4.2.16 on 2024-11-09 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aqt', '0008_remove_user_roleid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='RoleID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='aqt.role'),
            preserve_default=False,
        ),
    ]
