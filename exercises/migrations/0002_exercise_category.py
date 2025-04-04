# Generated by Django 5.1.7 on 2025-03-21 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='category',
            field=models.CharField(blank=True, choices=[('cardio', 'Cardio'), ('strength', 'Strength'), ('flexibility', 'Flexibility'), ('balance', 'Balance')], help_text='General exercise category (e.g., cardio, strength, flexibility, balance).', max_length=50),
        ),
    ]
