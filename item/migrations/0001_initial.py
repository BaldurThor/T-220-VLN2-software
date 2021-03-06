# Generated by Django 4.0.4 on 2022-05-02 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField()),
                ('name', models.CharField(max_length=191)),
                ('description', models.TextField()),
                ('image_url', models.CharField(max_length=191)),
                ('zip', models.CharField(max_length=191)),
                ('sold_at', models.DateField(null=True)),
                ('published_at', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('accepted', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('full_name', models.CharField(max_length=191)),
                ('street_name', models.CharField(max_length=191)),
                ('house_number', models.CharField(max_length=191)),
                ('city', models.CharField(max_length=191)),
                ('zip', models.CharField(max_length=191)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.country')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='item.item')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='item.offer')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='accepted_offer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_offer', to='item.offer'),
        ),
        migrations.AddField(
            model_name='item',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='item.condition'),
        ),
        migrations.AddField(
            model_name='item',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.country'),
        ),
        migrations.CreateModel(
            name='CategoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.category')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item')),
            ],
        ),
    ]
