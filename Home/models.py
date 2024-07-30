from django.db import models
from django.contrib.auth.models import User

# Create your models here. (tao csdl)
class CauThu(models.Model):
    ma_cau_thu = models.CharField(max_length = 3, primary_key = True, blank = False)
    ten_cau_thu = models.CharField(max_length = 50, null = True, blank = False)
    ngay_sinh = models.DateField(null = True, blank = False)
    loai_cau_thu = models.CharField(max_length = 50, null = True, blank = False)
    ghi_chu = models.CharField(max_length = 50, null = True, blank = True)

    
    # dat ten cho bang
    class Meta:       
        verbose_name_plural = 'Cau Thu'


# class Doi(models.Model):
#     ma_cau_thu = models.CharField(max_length = 3, primary_key = True, blank = False)
#     ten_cau_thu = models.CharField(max_length = 50, null = True, blank = False)
#     ngay_sinh = models.DateField(null = True, blank = False)
#     loai_cau_thu = models.CharField(max_length = 50, null = True, blank = False)
#     ghi_chu = models.CharField(max_length = 50, null = True, blank = True)

    
#     # dat ten cho bang
#     class Meta:       
#         verbose_name_plural = 'Doi'
    