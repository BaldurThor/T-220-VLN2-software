# Generated by Django 4.0.4 on 2022-05-03 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_userprofile_avg_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image_url',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
    ]
