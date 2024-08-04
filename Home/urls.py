from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('TruyXuatCauThu/', views.TruyXuatCauThu, name = 'TruyXuatCauThu'),
    path('TiepNhanHoSo/', views.TiepNhanHoSo, name = 'TiepNhanHoSo'),
    path('DangKiCauThu/', views.DangKiCauThu, name = 'DangKiCauThu'),
    path('ThongBao/', views.ThongBao, name = 'ThongBao'),
    path('ThayDoiQuyDinh/', views.ThayDoiQuyDinh, name = 'ThayDoiQuyDinh'),
]