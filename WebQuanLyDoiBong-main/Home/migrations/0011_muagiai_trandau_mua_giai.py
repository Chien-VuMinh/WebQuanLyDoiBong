# Generated by Django 5.0.7 on 2024-08-31 13:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Home", "0010_remove_ketqua_cau_thu_remove_ketqua_doi_ghi_ban_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="MuaGiai",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ten_mua_giai", models.CharField(max_length=100)),
                ("ngay_bat_dau", models.DateField()),
                ("ngay_ket_thuc", models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name="trandau",
            name="mua_giai",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="Home.muagiai",
            ),
        ),
    ]
