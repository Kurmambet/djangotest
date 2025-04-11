# Generated by Django 5.1.7 on 2025-04-10 08:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pract', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_changes', to=settings.AUTH_USER_MODEL, verbose_name='Редактировал'),
        ),
        migrations.AddField(
            model_name='goods',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products_by_cat', to='pract.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='goods',
            name='sup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products_by_sup', to='pract.supplier', verbose_name='Поставщик'),
        ),
        migrations.AddIndex(
            model_name='goods',
            index=models.Index(fields=['time_create'], name='pract_goods_time_cr_2d8c5b_idx'),
        ),
    ]
