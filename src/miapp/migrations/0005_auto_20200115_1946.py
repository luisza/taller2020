# Generated by Django 3.0.2 on 2020-01-15 19:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0004_auto_20200115_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggression',
            name='note_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de la nota'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggression',
            name='year',
            field=models.SmallIntegerField(default=2020, verbose_name='Año'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aggressor',
            name='victimRel',
            field=models.TextField(null=True, verbose_name='Relacion con victima'),
        ),
    ]
