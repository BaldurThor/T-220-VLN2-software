# Generated by Django 4.0.4 on 2022-05-02 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_alter_category_name_alter_condition_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='item',
            name='accepted_offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_offer', to='item.offer'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sold_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
