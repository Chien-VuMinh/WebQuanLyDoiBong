# Generated by Django 5.0.7 on 2024-07-30 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ma_cau_thu', models.CharField(max_length=3)),
                ('ten_cau_thu', models.CharField(max_length=50, null=True)),
                ('ngay_sinh', models.DateField(null=True)),
                ('loai_cau_thu', models.CharField(max_length=50, null=True)),
                ('ghi_chu', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
