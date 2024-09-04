from django.shortcuts import render, redirect, Http404
from django.http import HttpResponse

from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from datetime import datetime, date
from django.utils import timezone
from django.shortcuts import get_object_or_404


with open("regulation.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    AGE                         = list(map(int, lines[0].split()))
    SO_LUONG_CAU_THU            = list(map(int, lines[1].split()))
    SO_LUONG_CAU_THU_NGOAI_QUOC = list(map(int, lines[2].split()))
    THOI_DIEM_GHI_BAN_TOI_DA = lines[5].strip()
    LOAIBANTHANG = [line.strip() for line in lines[6:]]
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
    global NOIBINH, NGOAIBINH, DOI, COUNTNOIBINH, COUNTNGOAIBINH

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
        
        elif Doi.objects.filter(ten_doi_bong = ten_doi).exists():
            messages.info(request, 'Tên đội đã tồn tại')
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
            COUNTNOIBINH, COUNTNGOAIBINH = 1, 0

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
        ghichu    = "Nội binh" if COUNTNGOAIBINH == 0 else "Ngoại binh"

    
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
                CauThu.objects.create(ma_cau_thu = macauthu, ten_cau_thu = tencauthu, ngay_sinh = ngaysinh, loai_cau_thu = vitri, ghi_chu = ghichu, doi = DOI)
                return render(request, 'ThongBao.html', {'messages' : [DOI.ten_doi_bong], 'danh_sach_cau_thu' : CauThu.objects.filter(doi = DOI)})
            
            CauThu.objects.create(ma_cau_thu = macauthu, ten_cau_thu = tencauthu, ngay_sinh = ngaysinh, loai_cau_thu = vitri, ghi_chu = ghichu, doi = DOI)
        

        return render(request, 'DangKiCauThu.html') 

    else:
        messages.info(request, 'Nhập thông tin cầu thủ thứ 1')
        return render(request, 'DangKiCauThu.html')
DIEM_THANG = 3
DIEM_HOA = 2
DIEM_THUA = 1
XEP_HANG = 'macdinh'


def ThongBao(request):
    return render(request, 'ThongBao.html')


def ThayDoiQuyDinh(request):
    global SO_LUONG_CAU_THU_NGOAI_QUOC, SO_LUONG_CAU_THU, AGE, LOAIBANTHANG, THOI_DIEM_GHI_BAN_TOI_DA, DIEM_THANG, DIEM_HOA, DIEM_THUA, XEP_HANG

    if request.method == "POST":
        QuyDinh = request.POST['QuyDinh']

        if QuyDinh == 'tuoi':
            return render(request, 'ThayDoiQuyDinh.html', {'tuoi' : ['tuoi'], 'messages' : ['Nhập độ tuổi mới']})
        elif QuyDinh == 'thaydoituoi':
            AGE = [int(request.POST['tuoitoithieu']), int(request.POST['tuoitoida'])]
            return render(request, 'ThayDoiQuyDinh.html')
        
        elif QuyDinh == 'thoidiemghiban':
            return render(request, 'ThayDoiQuyDinh.html', {'thoidiemghiban' : ['thoidiemghiban'], 'messages' : ['Nhập thời điểm ghi bàn tối đa mới']})
        elif QuyDinh == 'thaydoithoidiemghiban':
            THOI_DIEM_GHI_BAN_TOI_DA = request.POST['thoidiemghiban']
            return render(request, 'ThayDoiQuyDinh.html')

        elif QuyDinh == 'soluong':
            return render(request, 'ThayDoiQuyDinh.html', {'soluong' : ['soluong'], 'messages' : ['Nhập số lượng cầu thủ mới']})
        elif QuyDinh == 'thaydoisl':
            SO_LUONG_CAU_THU = [int(request.POST['sltoithieu']), int(request.POST['sltoida'])]
            return render(request, 'ThayDoiQuyDinh.html')
        
        elif QuyDinh == 'diemso':
            return render(request, 'ThayDoiQuyDinh.html', {'diemso': ['diemso'], 'messages': ['Nhập số điểm cho Thắng, Hòa, Thua']})
        elif QuyDinh == 'thaydoidiemso':
            DIEM_THANG = int(request.POST['diem_thang'])
            DIEM_HOA = int(request.POST['diem_hoa'])
            DIEM_THUA = int(request.POST['diem_thua'])


            # Kiểm tra nếu vi phạm quy định Thắng > Hòa > Thua
            if not (DIEM_THANG > DIEM_HOA > DIEM_THUA):
                return render(request, 'ThayDoiQuyDinh.html', {'error': 'Quy định vi phạm: Điểm Thắng phải lớn hơn Hòa, và Hòa phải lớn hơn Thua.'})
            return render(request, 'ThayDoiQuyDinh.html')

        elif QuyDinh == 'xephang':
            return render(request, 'ThayDoiQuyDinh.html', {'xephang': ['xephang'], 'messages': ['Chọn thứ tự ưu tiên cho xếp hạng']})
        elif QuyDinh == 'thaydoixh':
            XEP_HANG = str(request.POST['xep_hang'])

            return render(request, 'ThayDoiQuyDinh.html')
        elif QuyDinh == 'soluongbanthang':
            return render(request, 'ThayDoiQuyDinh.html', {'soluongbanthang': ['soluongbanthang'], 'messages': ['Nhập danh sách loại bàn thắng', 'Cách nhau bởi dấu phẩy'], 'LOAIBANTHANG': LOAIBANTHANG})
        elif QuyDinh == 'thaydoisoluongbanthang':
            loaibanthang_str = request.POST.get('loaibanthang')
            LOAIBANTHANG = [loai.strip() for loai in loaibanthang_str.split(',')]
            return render(request, 'ThayDoiQuyDinh.html')
        
        elif QuyDinh == 'ngoaiquoc':
            return render(request, 'ThayDoiQuyDinh.html', {'ngoaiquoc' : ['ngoaiquoc'], 'messages' : ['Nhập số lượng cầu thủ ngoại quốc mới']})
        elif QuyDinh == 'thaydoingoaiquoc': 
            SO_LUONG_CAU_THU_NGOAI_QUOC[1] = int(request.POST['ngoaiquoc'])
            return render(request, 'ThayDoiQuyDinh.html')
        
        elif QuyDinh == 'luu':
            if MuaGiai.objects.exists():
            # Nếu có mùa giải, không cho phép thay đổi quy định
                # return render(request, 'ThayDoiQuyDinh.html', {'message': 'Không thể thay đổi quy định khi mùa giải đã bắt đầu.'})
                messages.error(request, 'Không thể thay đổi quy định khi mùa giải đã bắt đầu')
                return redirect('ThayDoiQuyDinh')
            f = open("regulation.txt", "w", encoding="utf-8")
            f.write(str(AGE[0]) + ' ' + str(AGE[1]) + '\n')
            f.write(str(SO_LUONG_CAU_THU[0]) + ' ' + str(SO_LUONG_CAU_THU[1]) + '\n')
            f.write(str(SO_LUONG_CAU_THU_NGOAI_QUOC[0]) + ' ' + str(SO_LUONG_CAU_THU_NGOAI_QUOC[1]) + '\n')
            f.write(str(DIEM_THANG)+ ' '+ str(DIEM_HOA)+ ' '+ str(DIEM_THUA) + '\n')
            f.write(str(XEP_HANG)+'\n')
            f.write(str(THOI_DIEM_GHI_BAN_TOI_DA) + '\n')
            for loai in LOAIBANTHANG:
                f.write(loai + '\n')
            f.close()
            return render(request, 'Home.html')

    return render(request, 'ThayDoiQuyDinh.html')

def LichThiDau(request):
    # Fetch all scheduled matches
    try:
        current_season = MuaGiai.objects.latest('ngay_bat_dau')
    except MuaGiai.DoesNotExist:
        return redirect('TaoMuaGiai')  # Redirect to a view to create a new season

    tran_daus = TranDau.objects.filter(mua_giai=current_season)
    print(tran_daus)  # Debugging: Print to console or log
    return render(request, 'LichThiDau.html', {'tran_daus': tran_daus, 'mua_giai': current_season})

def TaoMuaGiai(request):
    if request.method == "POST":
        ten_mua_giai = request.POST['ten_mua_giai']
        ngay_bat_dau = request.POST['ngay_bat_dau']
        ngay_ket_thuc = request.POST['ngay_ket_thuc']

        MuaGiai.objects.create(ten_mua_giai=ten_mua_giai, ngay_bat_dau=ngay_bat_dau, ngay_ket_thuc=ngay_ket_thuc)
        return redirect('LichThiDau')

    return render(request, 'TaoMuaGiai.html')

def XoaMuaGiai(request, mua_giai_id):
    try:
        # Retrieve the season
        mua_giai = get_object_or_404(MuaGiai, id=mua_giai_id)

        # Lấy danh sách các đội bóng thuộc mùa giải này
        doi_list = Doi.objects.all()
        
        # Reset số bàn thắng của tất cả cầu thủ của các đội bóng thuộc mùa giải này
        for doi in doi_list:
            cau_thu_list = CauThu.objects.filter(doi=doi)
            cau_thu_list.update(so_ban_thang=0)
        
        # Delete all matches related to the season
        TranDau.objects.filter(mua_giai=mua_giai).delete()
        
        KetQua.objects.all().delete()

        # Delete the season
        mua_giai.delete()
        
        # Show success message
        messages.success(request, "Đã xóa mùa giải và các trận đấu liên quan thành công.")
        
        # Redirect to create new season page
        return redirect('TaoMuaGiai')

    except MuaGiai.DoesNotExist:
        messages.error(request, "Mùa giải không tồn tại.")
        return redirect('LichThiDau')

def ThemTranDau(request):

    current_season = MuaGiai.objects.latest('ngay_bat_dau')

    if request.method == "POST":
        doi_nha_ma = request.POST.get('doi_nha')
        doi_khach_ma = request.POST['doi_khach']
        ngay_thi_dau = request.POST['ngay_thi_dau']
        gio_thi_dau = request.POST['gio_thi_dau']

        # Debugging information
        print(f"doi_nha_ma: {doi_nha_ma}")  

        try:
            doi_nha = Doi.objects.get(ma_doi_bong=doi_nha_ma)
            doi_khach=Doi.objects.get(ma_doi_bong=doi_khach_ma)
            san_dau = doi_nha.san_nha
        except Doi.DoesNotExist:
            messages.error(request, "Đội nhà không tồn tại.")
            return redirect('ThemTranDau')

        # 1. Check if the home team is the same as the away team
        if doi_nha == doi_khach:
            messages.error(request, 'Đội nhà và đội khách không thể là cùng một đội.')
            return redirect('ThemTranDau')

        # 2. Check if match between these two teams already exists in the season
        if TranDau.objects.filter(doi_nha=doi_nha, doi_khach=doi_khach, mua_giai=current_season).exists():
            messages.error(request, 'Trận đấu giữa hai đội này đã được tạo trong mùa giải này.')
            return redirect('ThemTranDau')

        current_time = datetime.now()
        current_time = timezone.make_aware(current_time, timezone.get_current_timezone())

        # 3. Check if the match date is within the season's start and end dates
        ngay_thi_dau = datetime.strptime(ngay_thi_dau, '%Y-%m-%d').date()
        gio_thi_dau = datetime.strptime(gio_thi_dau, '%H:%M').time()
        match_datetime = datetime.combine(ngay_thi_dau, gio_thi_dau)

        # Convert match_datetime to an aware datetime
        match_datetime = timezone.make_aware(match_datetime, timezone.get_current_timezone())

        if match_datetime.date() < current_season.ngay_bat_dau or match_datetime.date() > current_season.ngay_ket_thuc:
            messages.error(request, 'Ngày thi đấu phải nằm trong khoảng thời gian của mùa giải.')
            return redirect('ThemTranDau')

        # 4. Check if the match date is in the future
        if match_datetime <= current_time:
            messages.error(request, 'Ngày giờ thi đấu phải sau thời gian hiện tại.')
            return redirect('ThemTranDau')

        # Assuming valid data
        TranDau.objects.create(
            doi_nha=doi_nha,
            doi_khach=doi_khach,
            ngay_thi_dau=ngay_thi_dau,
            gio_thi_dau=gio_thi_dau,
            san_dau=san_dau,
            mua_giai=current_season
        )
        return redirect('LichThiDau')

    else:
        doi_bongs = Doi.objects.all()
        return render(request, 'ThemTranDau.html', {'doi_bongs': doi_bongs})

def GhiNhanKetQua(request):
    global THOI_DIEM_GHI_BAN_TOI_DA
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
            return redirect('GhiNhanKetQua')
        try:
            tran_dau = TranDau.objects.get(doi_nha=doi_1, doi_khach=doi_2, ngay_thi_dau=ngay, gio_thi_dau=gio)
        except TranDau.DoesNotExist:
            messages.error(request, "Trận đấu không tồn tại.")
            return redirect('GhiNhanKetQua')
        try:
            ty_so_x, ty_so_y = map(int, ty_so.split(':'))
            if ty_so_x < 0 or ty_so_y < 0:
                raise ValueError("Tỷ số không được âm.")
        except (ValueError, IndexError):
            messages.error(request, "Tỷ số không hợp lệ. Vui lòng nhập tỷ số theo định dạng x:y và không âm.")
            return redirect('GhiNhanKetQua')

        # Xử lý danh sách cầu thủ ghi bàn
        ban_thang = []
        so_ban_thang = int(request.POST.get('so_ban_thang', 0))
        for i in range(1, so_ban_thang + 1):
            cau_thu_id = request.POST.get(f'cau_thu_{i}')
            doi_ghi_ban_ma = request.POST.get(f'doi_ghi_ban_{i}')
            loai_ban_thang = request.POST.get(f'loai_ban_thang_{i}')
            thoi_diem = int(request.POST.get(f'thoi_diem_{i}'))

            # Kiểm tra thời điểm ghi bàn
            if thoi_diem > int(THOI_DIEM_GHI_BAN_TOI_DA):
                messages.error(request, f"Thời điểm ghi bàn số {i} không được vượt quá {THOI_DIEM_GHI_BAN_TOI_DA} phút.")
                return redirect('GhiNhanKetQua')
             # Kiểm tra cầu thủ có thuộc đội bóng ghi bàn hoặc đội bóng bị ghi bàn không
            try:
                cau_thu = CauThu.objects.get(pk=cau_thu_id)
                doi_ghi_ban = Doi.objects.get(ma_doi_bong=doi_ghi_ban_ma)

                # Kiểm tra cầu thủ có thuộc đội bóng ghi bàn
                if cau_thu.doi != doi_ghi_ban:
                    messages.error(request, f"Cầu thủ số ghi bàn {i} không thuộc đội bóng của cầu thủ")
                    return redirect('GhiNhanKetQua')
            except (CauThu.DoesNotExist, Doi.DoesNotExist):
                messages.error(request, f"Dữ liệu cầu thủ số {i} không hợp lệ.")
                return redirect('GhiNhanKetQua')
            try:
                cau_thu = CauThu.objects.get(pk=cau_thu_id)
                doi_ghi_ban = Doi.objects.get(ma_doi_bong=doi_ghi_ban_ma)
                # Cập nhật số bàn thắng cho cầu thủ
                cau_thu.so_ban_thang += 1
                cau_thu.save()

            except (CauThu.DoesNotExist, Doi.DoesNotExist):
                messages.error(request, f"Dữ liệu cầu thủ số {i} không hợp lệ.")
                return redirect('GhiNhanKetQua')

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
    with open("regulation.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        diem_thang, diem_hoa, diem_thua = map(int, lines[3].strip().split())
        xep_hang = lines[4].strip()  # Đọc quy tắc xếp hạng từ dòng thứ 5 của file
    bang_xep_hang = {}
    doi_bong_list = Doi.objects.all()

    for doi in doi_bong_list:
        bang_xep_hang[doi.ma_doi_bong] = {
            'ma_doi_bong': doi.ma_doi_bong,
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
            bang_xep_hang[doi_1.ma_doi_bong]['diem'] += diem_thang
            bang_xep_hang[doi_2.ma_doi_bong]['thua'] += 1
            bang_xep_hang[doi_2.ma_doi_bong]['diem'] += diem_thua
        elif ty_so_1 < ty_so_2:
            bang_xep_hang[doi_2.ma_doi_bong]['thang'] += 1
            bang_xep_hang[doi_2.ma_doi_bong]['diem'] += diem_thang
            bang_xep_hang[doi_1.ma_doi_bong]['thua'] += 1
            bang_xep_hang[doi_1.ma_doi_bong]['diem'] += diem_thua
        else:
            bang_xep_hang[doi_1.ma_doi_bong]['hoa'] += 1
            bang_xep_hang[doi_1.ma_doi_bong]['diem'] += diem_hoa
            bang_xep_hang[doi_2.ma_doi_bong]['hoa'] += 1
            bang_xep_hang[doi_2.ma_doi_bong]['diem'] += diem_hoa
    # Chuyển đổi sang danh sách
    bang_xep_hang_list = list(bang_xep_hang.values())

    # Lấy danh sách 5 cầu thủ ghi bàn nhiều nhất
    # Sắp xếp danh sách theo quy tắc ưu tiên
    if xep_hang == 'ban_thang_sotran_banthua':
        bang_xep_hang_list.sort(key=lambda x: (-x['diem'],-x['ban_thang'], -x['tran'], x['ban_thua']))
    elif xep_hang == 'ban_thua_banthang_sotran':
        bang_xep_hang_list.sort(key=lambda x: (-x['diem'],x['ban_thua'], -x['ban_thang'], -x['tran']))
    elif xep_hang == 'sotran_banthang_banthua':
        bang_xep_hang_list.sort(key=lambda x: (-x['diem'],-x['tran'], -x['ban_thang'], x['ban_thua']))
    elif xep_hang == 'macdinh':  # Mặc định là xếp theo điểm số
        bang_xep_hang_list.sort(key=lambda x: (-x['diem'], -x['ban_thang'], x['ban_thua'],-x['tran']))

    top_scorers = CauThu.objects.order_by('-so_ban_thang')[:5]

    return render(request, 'BangXepHang.html', {
        'bang_xep_hang_list': bang_xep_hang_list,
        'top_scorers': top_scorers
    })

def ChiTietDoi(request, ma_doi_bong):
    try:
        doi_bong = Doi.objects.get(ma_doi_bong=ma_doi_bong)
    except Doi.DoesNotExist:
        raise Http404("Đội bóng không tồn tại")
    return render(request, 'ChiTietDoi.html', {'doi_bong': doi_bong})
def lay_tran_dau(request):
    doi_1_id = request.GET.get('doi_1')
    doi_2_id = request.GET.get('doi_2')

    tran_dau = TranDau.objects.all()

    if doi_1_id:
        tran_dau = tran_dau.filter(doi_nha__ma_doi_bong=doi_1_id)
    if doi_2_id:
        tran_dau = tran_dau.filter(doi_khach__ma_doi_bong=doi_2_id)

    tran_dau_list = list(tran_dau.values('doi_nha_id', 'doi_nha__ten_doi_bong', 'doi_khach_id', 'doi_khach__ten_doi_bong', 'san_dau', 'ngay_thi_dau', 'gio_thi_dau'))
    return JsonResponse(tran_dau_list, safe=False)
def lay_loai_ban_thang(request):
    return JsonResponse(LOAIBANTHANG, safe=False)
def lay_cau_thu_theo_doi(request):
    doi_bong_id = request.GET.get('doi_bong_id')
    cau_thus = CauThu.objects.filter(doi_id=doi_bong_id).values('ma_cau_thu', 'ten_cau_thu') 
    cau_thu_dict = {str(cau_thu['ma_cau_thu']): cau_thu for cau_thu in cau_thus}
    return JsonResponse(cau_thu_dict)
