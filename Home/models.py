from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here. (tao csdl)
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
        return f"{self.ma_cau_thu} : {self.ten_cau_thu} : {self.doi.ten_doi_bong}"
    # dat ten cho bang
    class Meta:
        verbose_name_plural = 'Cầu Thủ'
