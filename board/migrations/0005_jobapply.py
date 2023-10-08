# Generated by Django 4.2.4 on 2023-10-06 03:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0004_curriculum_cv_dob_curriculum_cv_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApply',
            fields=[
                ('apply_id', models.AutoField(primary_key=True, serialize=False)),
                ('motivation', models.TextField(blank=True, max_length=700)),
                ('applydate', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sourcejob', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.jobposition')),
            ],
        ),
    ]