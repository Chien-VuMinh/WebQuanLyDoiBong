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
    path('TaoMuaGiai/', views.TaoMuaGiai, name='TaoMuaGiai'),
    path('lich-thi-dau/', views.LichThiDau, name='LichThiDau'),
    path('them-tran-dau/', views.ThemTranDau, name='ThemTranDau'),
    path('GhiNhanKetQua/', views.GhiNhanKetQua, name='GhiNhanKetQua'),
    path('bang-xep-hang/', views.BangXepHang, name='BangXepHang'),
    path('doi/<str:ma_doi_bong>/', views.ChiTietDoi, name='ChiTietDoi'),
]
