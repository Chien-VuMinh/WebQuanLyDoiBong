# Generated by Django 5.1 on 2024-08-20 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0009_ketqua_delete_ghinhanketqua'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ketqua',
            name='cau_thu',
        ),
        migrations.RemoveField(
            model_name='ketqua',
            name='doi_ghi_ban',
        ),
        migrations.RemoveField(
            model_name='ketqua',
            name='loai_ban_thang',
        ),
        migrations.RemoveField(
            model_name='ketqua',
            name='thoi_diem',
        ),
        migrations.AddField(
            model_name='ketqua',
            name='ban_thang',
            field=models.JSONField(default=list),
        ),
    ]
