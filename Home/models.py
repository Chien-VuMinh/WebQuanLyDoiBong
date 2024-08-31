from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here. (tao csdl)
from django.db.models import JSONField

class Doi(models.Model):
    ma_doi_bong     = models.CharField(max_length = 3, primary_key = True, blank = False)
    ten_doi_bong    = models.CharField(max_length = 50, blank = False)
    san_nha         = models.CharField(max_length = 50, blank = False)
    so_luong_cau_thu= models.IntegerField(blank = False)
    ngoai_quoc      = models.CharField(max_length = 50, null = True, blank = True)

    

    def __str__(self):
        return f"{self.ma_doi_bong} : {self.ten_doi_bong}"
    
    # dat ten cho bang
    class Meta:       
        verbose_name_plural = 'Đội'
    


class CauThu(models.Model):
    ma_cau_thu      = models.CharField(max_length = 3, primary_key = True, blank = False)
    ten_cau_thu     = models.CharField(max_length = 50, null = True, blank = False)
    ngay_sinh       = models.DateField(null = True, blank = False)
    loai_cau_thu    = models.CharField(max_length = 50, null = True, blank = False)
    ghi_chu         = models.CharField(max_length = 50, null = True, blank = True)
    doi             = models.ForeignKey(Doi, on_delete = models.SET_NULL,  null = True, blank = False)

    

    def __str__(self):
        return f"{self.ma_cau_thu} : {self.ten_cau_thu} : {self.doi}"
    # dat ten cho bang
    class Meta:
        verbose_name_plural = 'Cầu Thủ'

class TranDau(models.Model):
    doi_nha = models.ForeignKey(Doi, related_name='doi_nha', on_delete=models.CASCADE)
    doi_khach = models.ForeignKey(Doi, related_name='doi_khach', on_delete=models.CASCADE)
    ngay_thi_dau = models.DateField()
    gio_thi_dau = models.TimeField()
    san_dau = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.doi_nha.ten_doi_bong} vs {self.doi_khach.ten_doi_bong} on {self.ngay_thi_dau}"

class KetQua(models.Model):
    doi_1 = models.ForeignKey(Doi, related_name='ghi_nhan_doi_1', on_delete=models.CASCADE)
    doi_2 = models.ForeignKey(Doi, related_name='ghi_nhan_doi_2', on_delete=models.CASCADE)
    ty_so = models.CharField(max_length=5, default="0-0")
    san = models.CharField(max_length=255)
    ngay = models.DateField()
    gio = models.TimeField()
    ban_thang = JSONField(default=list)

    LOAI_BAN_THANG = (
        ('THUONG', 'Bàn thắng thường'),
        ('PHAT_DEN', 'Penalty'),
        ('TU_CUOI', 'Phản lưới nhà'),
    )

    def __str__(self):
        return f"{self.doi_1.ten_doi_bong} {self.ty_so} {self.doi_2.ten_doi_bong}"

    class Meta:
        verbose_name_plural = 'Ghi Nhận Kết Quả'