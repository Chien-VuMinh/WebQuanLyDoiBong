from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from datetime import datetime, date



f = open("regulation.txt", "r")
lines = f.readlines()
AGE                         = list(map(int, lines[0].split()))
SO_LUONG_CAU_THU            = list(map(int, lines[1].split()))
SO_LUONG_CAU_THU_NGOAI_QUOC = list(map(int, lines[2].split()))
f.close()

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
    global NOIBINH, NGOAIBINH, DOI

    if request.method == "POST":
        ma_doi = request.POST['madoi']
        ten_doi = request.POST['tendoi']
        so_luong = int(request.POST['soluong'])
        ngoai_quoc = int(request.POST['ngoaiquoc'])
        san_nha = request.POST['sannha']

        if len(ma_doi) != 3:
            messages.info(request, 'Mã đội phải là mã 3 ký tự')
            return redirect('TiepNhanHoSo')
        
        elif Doi.objects.filter(ma_doi_bong = ma_doi).exists():
            messages.info(request, 'Mã đội đã tồn tại')
            return redirect('TiepNhanHoSo')

        elif Doi.objects.filter(san_nha = san_nha).exists():
            messages.info(request, 'Sân nhà đã có người đăng ký')
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
            Doi.objects.create(ma_doi_bong = ma_doi, ten_doi_bong = ten_doi, san_nha = san_nha, so_luong_cau_thu = so_luong, ngoai_quoc = ngoai_quoc).save()
            DOI = Doi.objects.get(ma_doi_bong = ma_doi)           
            NOIBINH = so_luong - ngoai_quoc
            NGOAIBINH = ngoai_quoc

            return redirect('DangKiCauThu')



    else:
        return render(request, 'TiepNhanHoSo.html')
    


def YearDiff(d):
    current_day = date.today()
    return int(abs(current_day - d).days / (365))


def DangKiCauThu(request):
    global NOIBINH, NGOAIBINH, COUNTNOIBINH, COUNTNGOAIBINH, DOI
    
    if request.method == "POST":
        macauthu    = request.POST['macauthu']
        tencauthu    = request.POST['tencauthu']  
        ngaysinh    = datetime.strptime(request.POST['ngaysinh'], '%Y-%m-%d').date()
        vitri    = request.POST['vitri']  
        ghichu    = "Nội binh" if NOIBINH != 0 else "Ngoại binh"

    
        if len(macauthu) != 3:
            messages.info(request, 'Mã cầu thủ là mã 3 ký tự')
            return render(request, 'DangKiCauThu.html')

        elif CauThu.objects.filter(ma_cau_thu = macauthu).exists():
            messages.info(request, 'Mã cầu thủ đã tồn tại')
            return render(request, 'DangKiCauThu.html')
        
        elif not (AGE[0] <= YearDiff(ngaysinh) <= AGE[1]):
            print(YearDiff(ngaysinh))
            messages.info(request, f"""Ngày sinh cần phải nằm trong khoảng 
                                       [{AGE[0]}, {AGE[1]}]""")
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

                messages.info(request, 'Nhập thông tin cầu thủ ngoại binh thứ ' + str(COUNTNGOAIBINH))   

            else:
                messages.info(request, 'Đăng ký thành công')   
                CauThu.objects.create(ma_cau_thu = macauthu, ten_cau_thu = tencauthu, ngay_sinh = ngaysinh, loai_cau_thu = vitri, ghi_chu = ghichu, doi = DOI)
                return render(request, 'ThongBao.html', {'messages' : [DOI.ten_doi_bong], 'danh_sach_cau_thu' : CauThu.objects.filter(doi = DOI)})
            
            CauThu.objects.create(ma_cau_thu = macauthu, ten_cau_thu = tencauthu, ngay_sinh = ngaysinh, loai_cau_thu = vitri, ghi_chu = ghichu, doi = DOI)
        

        return render(request, 'DangKiCauThu.html') 

    else:
        messages.info(request, 'Nhập thông tin cầu thủ thứ 1')
        return render(request, 'DangKiCauThu.html')
    

def ThongBao(request):
    return render(request, 'ThongBao.html')


def ThayDoiQuyDinh(request):
    global SO_LUONG_CAU_THU_NGOAI_QUOC, SO_LUONG_CAU_THU, AGE

    if request.method == "POST":
        QuyDinh = request.POST['QuyDinh']

        if QuyDinh == 'tuoi':
            return render(request, 'ThayDoiQuyDinh.html', {'tuoi' : ['tuoi'], 'messages' : ['Nhập độ tuổi mới']})
        elif QuyDinh == 'thaydoituoi':
            AGE = [int(request.POST['tuoitoithieu']), int(request.POST['tuoitoida'])]
            return render(request, 'ThayDoiQuyDinh.html')
        
        elif QuyDinh == 'soluong':
            return render(request, 'ThayDoiQuyDinh.html', {'soluong' : ['soluong'], 'messages' : ['Nhập số lượng cầu thủ mới']})
        elif QuyDinh == 'thaydoisl':
            SO_LUONG_CAU_THU = [int(request.POST['sltoithieu']), int(request.POST['sltoida'])]
            return render(request, 'ThayDoiQuyDinh.html')
        
        elif QuyDinh == 'ngoaiquoc':
            return render(request, 'ThayDoiQuyDinh.html', {'ngoaiquoc' : ['ngoaiquoc'], 'messages' : ['Nhập số lượng cầu thủ ngoại quốc mới']})
        elif QuyDinh == 'thaydoingoaiquoc':
            SO_LUONG_CAU_THU_NGOAI_QUOC = int(request.POST['ngoaiquoc'])
            return render(request, 'ThayDoiQuyDinh.html')
        
        elif QuyDinh == 'luu':
            f = open("regulation.txt", "w")
            f.write(str(AGE[0]) + ' ' + str(AGE[1]) + '\n')
            f.write(str(SO_LUONG_CAU_THU[0]) + ' ' + str(SO_LUONG_CAU_THU[1]) + '\n')
            f.write(str(SO_LUONG_CAU_THU_NGOAI_QUOC[0]) + ' ' + str(SO_LUONG_CAU_THU_NGOAI_QUOC[1]))
            f.close()
            return render(request, 'Home.html')

    return render(request, 'ThayDoiQuyDinh.html')

def LichThiDau(request):
    # Fetch all scheduled matches
    tran_daus = TranDau.objects.all()

    context = {
        'tran_daus': tran_daus
    }
    return render(request, 'LichThiDau.html', context)


def ThemTranDau(request):
    if request.method == "POST":
        doi_nha_ma = request.POST.get('doi_nha')
        doi_khach = request.POST['doi_khach']
        ngay_thi_dau = request.POST['ngay_thi_dau']
        gio_thi_dau = request.POST['gio_thi_dau']

        # Debugging information
        print(f"doi_nha_ma: {doi_nha_ma}")  

        try:
            doi_nha = Doi.objects.get(ma_doi_bong=doi_nha_ma)
            san_dau = doi_nha.san_nha
        except Doi.DoesNotExist:
            messages.error(request, "Đội nhà không tồn tại.")
            return redirect('ThemTranDau')

        # Assuming valid data
        TranDau.objects.create(
            doi_nha=doi_nha,
            doi_khach=Doi.objects.get(ma_doi_bong=doi_khach),
            ngay_thi_dau=ngay_thi_dau,
            gio_thi_dau=gio_thi_dau,
            san_dau=san_dau
        )
        return redirect('LichThiDau')

    else:
        doi_bongs = Doi.objects.all()
        return render(request, 'ThemTranDau.html', {'doi_bongs': doi_bongs})

def GhiNhanKetQua(request):
    doi_bongs = Doi.objects.all()

    if request.method == 'POST':
        # Lấy thông tin trận đấu
        doi_1_ma = request.POST.get('doi_1')
        doi_2_ma = request.POST.get('doi_2')
        ty_so = request.POST.get('ty_so')
        san = request.POST.get('san')
        ngay = request.POST.get('ngay')
        gio = request.POST.get('gio')

        try:
            doi_1 = Doi.objects.get(ma_doi_bong=doi_1_ma)
            doi_2 = Doi.objects.get(ma_doi_bong=doi_2_ma)
        except Doi.DoesNotExist:
            messages.error(request, "Mã đội bóng không hợp lệ.")
            return redirect('ghi_nhan_ket_qua')

        # Xử lý danh sách cầu thủ ghi bàn
        ban_thang = []
        so_ban_thang = int(request.POST.get('so_ban_thang', 0))
        for i in range(1, so_ban_thang + 1):
            cau_thu_id = request.POST.get(f'cau_thu_{i}')
            doi_ghi_ban_ma = request.POST.get(f'doi_ghi_ban_{i}')
            loai_ban_thang = request.POST.get(f'loai_ban_thang_{i}')
            thoi_diem = int(request.POST.get(f'thoi_diem_{i}'))

            try:
                cau_thu = CauThu.objects.get(pk=cau_thu_id)
                doi_ghi_ban = Doi.objects.get(ma_doi_bong=doi_ghi_ban_ma)
            except (CauThu.DoesNotExist, Doi.DoesNotExist):
                messages.error(request, f"Dữ liệu cầu thủ số {i} không hợp lệ.")
                return redirect('ghi_nhan_ket_qua')

            ban_thang.append({
                'cau_thu': cau_thu_id,
                'doi_ghi_ban': doi_ghi_ban_ma,
                'loai_ban_thang': loai_ban_thang,
                'thoi_diem': thoi_diem
            })

        # Tạo mới KetQua với danh sách bàn thắng
        ket_qua = KetQua.objects.create(
            doi_1=doi_1,
            doi_2=doi_2,
            ty_so=ty_so,
            san=san,
            ngay=ngay,
            gio=gio,
            ban_thang=ban_thang
        )

        messages.success(request, "Ghi nhận kết quả thành công.")
        return redirect('GhiNhanKetQua')

    context = {
        'doi_bongs': doi_bongs,
    }
    return render(request, 'GhiNhanKetQua.html', context)

def BangXepHang(request):
    # Khởi tạo bảng xếp hạng cho các đội
    bang_xep_hang = {}
    doi_bong_list = Doi.objects.all()
    
    for doi in doi_bong_list:
        bang_xep_hang[doi.ma_doi_bong] = {
            'ten_doi_bong': doi.ten_doi_bong,
            'tran': 0,
            'thang': 0,
            'hoa': 0,
            'thua': 0,
            'ban_thang': 0,
            'ban_thua': 0,
            'diem': 0
        }

    # Lấy kết quả các trận đấu
    ket_qua_list = KetQua.objects.all()
    for ket_qua in ket_qua_list:
        doi_1 = ket_qua.doi_1
        doi_2 = ket_qua.doi_2
        
        # Sử dụng dấu phân cách đúng để tách tỷ số
        ty_so_1, ty_so_2 = map(int, ket_qua.ty_so.replace(':', '-').split('-'))

        # Cập nhật số trận đã đấu
        bang_xep_hang[doi_1.ma_doi_bong]['tran'] += 1
        bang_xep_hang[doi_2.ma_doi_bong]['tran'] += 1

        # Cập nhật số bàn thắng và bàn thua
        bang_xep_hang[doi_1.ma_doi_bong]['ban_thang'] += ty_so_1
        bang_xep_hang[doi_1.ma_doi_bong]['ban_thua'] += ty_so_2
        bang_xep_hang[doi_2.ma_doi_bong]['ban_thang'] += ty_so_2
        bang_xep_hang[doi_2.ma_doi_bong]['ban_thua'] += ty_so_1

        # Xác định kết quả trận đấu và cập nhật điểm số
        if ty_so_1 > ty_so_2:
            bang_xep_hang[doi_1.ma_doi_bong]['thang'] += 1
            bang_xep_hang[doi_1.ma_doi_bong]['diem'] += 3
            bang_xep_hang[doi_2.ma_doi_bong]['thua'] += 1
        elif ty_so_1 < ty_so_2:
            bang_xep_hang[doi_2.ma_doi_bong]['thang'] += 1
            bang_xep_hang[doi_2.ma_doi_bong]['diem'] += 3
            bang_xep_hang[doi_1.ma_doi_bong]['thua'] += 1
        else:
            bang_xep_hang[doi_1.ma_doi_bong]['hoa'] += 1
            bang_xep_hang[doi_1.ma_doi_bong]['diem'] += 1
            bang_xep_hang[doi_2.ma_doi_bong]['hoa'] += 1
            bang_xep_hang[doi_2.ma_doi_bong]['diem'] += 1

    # Chuyển đổi sang danh sách và sắp xếp theo điểm số và hiệu số bàn thắng
    bang_xep_hang_list = sorted(bang_xep_hang.values(), key=lambda x: (-x['diem'], x['ban_thang'] - x['ban_thua']))

    return render(request, 'BangXepHang.html', {'bang_xep_hang_list': bang_xep_hang_list})
