# Generated by Django 5.0.7 on 2024-07-31 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doi',
            fields=[
                ('ma_doi_bong', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('ten_doi_bong', models.CharField(max_length=50)),
                ('san_nha', models.CharField(max_length=50)),
                ('so_luong_cau_thu', models.IntegerField()),
                ('ngoai_quoc', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': 'Đội',
            },
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AlterModelOptions(
            name='cauthu',
            options={'verbose_name_plural': 'Cầu Thủ'},
        ),
        migrations.RemoveField(
            model_name='cauthu',
            name='id',
        ),
        migrations.AlterField(
            model_name='cauthu',
            name='ghi_chu',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cauthu',
            name='ma_cau_thu',
            field=models.CharField(max_length=3, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='doi',
            name='cau_thu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Home.cauthu'),
        ),
    ]
