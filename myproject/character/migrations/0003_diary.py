# Generated by Django 4.2.14 on 2024-07-18 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('character', '0002_character_final_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('entry_time', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('weather', models.CharField(choices=[('sunny', '맑음'), ('partly_cloudy', '약간 흐림'), ('cloudy', '흐림'), ('rain', '비'), ('snow', '눈')], max_length=20)),
                ('wake_up_time', models.TimeField()),
                ('sleep_time', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]