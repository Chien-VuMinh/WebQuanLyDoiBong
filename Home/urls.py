from django.contrib import admin
from django.urls import path, include
from . import views
from .views import XoaMuaGiai


urlpatterns = [
    path('', views.home, name = 'home'),
    path('TruyXuatCauThu/', views.TruyXuatCauThu, name = 'TruyXuatCauThu'),
    path('TiepNhanHoSo/', views.TiepNhanHoSo, name = 'TiepNhanHoSo'),
    path('DangKiCauThu/', views.DangKiCauThu, name = 'DangKiCauThu'),
    path('ThongBao/', views.ThongBao, name = 'ThongBao'),
    path('ThayDoiQuyDinh/', views.ThayDoiQuyDinh, name = 'ThayDoiQuyDinh'),
    path('TaoMuaGiai/', views.TaoMuaGiai, name='TaoMuaGiai'),
    path('xoa-mua-giai/<int:mua_giai_id>/', XoaMuaGiai, name='XoaMuaGiai'),
    path('lich-thi-dau/', views.LichThiDau, name='LichThiDau'),
    path('them-tran-dau/', views.ThemTranDau, name='ThemTranDau'),
    path('GhiNhanKetQua/', views.GhiNhanKetQua, name='GhiNhanKetQua'),
    path('lay-tran-dau/', views.lay_tran_dau, name='lay_tran_dau'),
    path('bang-xep-hang/', views.BangXepHang, name='BangXepHang'),
    path('doi/<str:ma_doi_bong>/', views.ChiTietDoi, name='ChiTietDoi'),
    path('lay-loai-ban-thang/', views.lay_loai_ban_thang, name='lay_loai_ban_thang'),
]
