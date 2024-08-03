from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from datetime import datetime


SO_LUONG_CAU_THU            = [0, 22]
SO_LUONG_CAU_THU_NGOAI_QUOC = [0, 3]

DOI = None
NGOAIBINH  = NOIBINH = 0
COUNTNOIBINH, COUNTNGOAIBINH = 1, 0


# Create your views here.
def home(request):
    context = {}
    return render(request, 'Home.html', context)


def TruyXuatCauThu(request):
    context = {}
    cau_thu = None
    danh_sach_cau_thu = None

    if request.method == "POST":
        cau_thu = request.POST['Search']
        if CauThu.objects.filter(ten_cau_thu__contains = cau_thu).exists():
            danh_sach_cau_thu = CauThu.objects.filter(ten_cau_thu__contains = cau_thu)

    
    return render(request, 'TruyXuatCauThu.html', {"searched" : cau_thu, "danh_sach_cau_thu" : danh_sach_cau_thu})


def TiepNhanHoSo(request):
    global NOIBINH, NGOAIBINH, COUNTNOIBINH, COUNTNGOAIBINH, DOI

    if request.method == "POST":
        ma_doi = request.POST['madoi']
        ten_doi = request.POST['tendoi']
        so_luong = int(request.POST['soluong'])
        ngoai_quoc = int(request.POST['ngoaiquoc'])

        if len(ma_doi) != 3:
            messages.info(request, 'Mã đội phải là mã 3 ký tự')
            return redirect('TiepNhanHoSo')
        
        elif Doi.objects.filter(ma_doi_bong = ma_doi).exists():
            messages.info(request, 'Mã đội đã tồn tại')
            return redirect('TiepNhanHoSo')
        
        elif not (SO_LUONG_CAU_THU[0] <= so_luong <= SO_LUONG_CAU_THU[1]):
            messages.info(request, f'''Số lượng cầu thủ cần phải nằm trong khoảng 
                                       [{SO_LUONG_CAU_THU[0]}, {SO_LUONG_CAU_THU[1]}]''')
            return redirect('TiepNhanHoSo')
        
        elif not (SO_LUONG_CAU_THU_NGOAI_QUOC[0] <= ngoai_quoc <= SO_LUONG_CAU_THU_NGOAI_QUOC[1]):
            messages.info(request, f"""Số lượng cầu thủ ngoại quốc cần phải nằm trong khoảng 
                                       [{SO_LUONG_CAU_THU_NGOAI_QUOC[0]}, {SO_LUONG_CAU_THU_NGOAI_QUOC[1]}]""")
            return redirect('TiepNhanHoSo')
        
        else: 
            Doi.objects.create(ma_doi_bong = ma_doi, ten_doi_bong = ten_doi, san_nha = "san nha", so_luong_cau_thu = so_luong, ngoai_quoc = ngoai_quoc).save()
            DOI = Doi.objects.get(ma_doi_bong = ma_doi)           
            NOIBINH = so_luong - ngoai_quoc
            NGOAIBINH = ngoai_quoc

            return redirect('DangKiCauThu')



    else:
        return render(request, 'TiepNhanHoSo.html')
    



def DangKiCauThu(request):
    global NOIBINH, NGOAIBINH, COUNTNOIBINH, COUNTNGOAIBINH, DOI
    
    if request.method == "POST":
        macauthu    = request.POST['macauthu']
        tencauthu    = request.POST['tencauthu']  
        ngaysinh    = request.POST['ngaysinh']
        vitri    = request.POST['vitri']  
        ghichu    = "Ngoại binh"

    
        if len(macauthu) != 3:
            messages.info(request, 'Mã cầu thủ là mã 3 ký tự')
            return render(request, 'DangKiCauThu.html')

        elif CauThu.objects.filter(ma_cau_thu = macauthu).exists():
            messages.info(request, 'Mã cầu thủ đã tồn tại')
            return render(request, 'DangKiCauThu.html')
        
        else:
            if COUNTNOIBINH < NOIBINH:
                COUNTNOIBINH += 1
                ghichu = "Nội binh"
                messages.info(request, 'Nhập thông tin cầu thủ thứ ' + str(COUNTNOIBINH))     

            elif COUNTNGOAIBINH < NGOAIBINH:   
                COUNTNGOAIBINH += 1
                
                if COUNTNOIBINH == NOIBINH:
                    ghichu = "Nội binh"
                    COUNTNOIBINH += 1
                else:
                    ghichu = "Ngoại binh"

                messages.info(request, 'Nhập thông tin cầu thủ ngoại bình thứ ' + str(COUNTNGOAIBINH))   

            else:
                messages.info(request, 'Đăng ký thành công')   
                CauThu.objects.create(ma_cau_thu = macauthu, ten_cau_thu = tencauthu, ngay_sinh = datetime.strptime(ngaysinh, '%Y-%m-%d').date(), loai_cau_thu = vitri, ghi_chu = ghichu, doi = DOI)
                return render(request, 'ThongBao.html', {'messages' : [DOI.ten_doi_bong], 'danh_sach_cau_thu' : CauThu.objects.filter(doi = DOI)})
            
            CauThu.objects.create(ma_cau_thu = macauthu, ten_cau_thu = tencauthu, ngay_sinh = datetime.strptime(ngaysinh, '%Y-%m-%d').date(), loai_cau_thu = vitri, ghi_chu = ghichu, doi = DOI)
        

        return render(request, 'DangKiCauThu.html') 

    else:
        messages.info(request, 'Nhập thông tin cầu thủ thứ 1')
        return render(request, 'DangKiCauThu.html')
    

def ThongBao(request):
    return render(request, 'ThongBao.html')