# Generated by Django 4.2.4 on 2023-10-07 23:09

import board.functions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_jobapply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapply',
            name='motivation',
            field=models.TextField(default='Why do you want to work for us?', max_length=700, validators=[board.functions.validate_motivation]),
        ),
    ]
