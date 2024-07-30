from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *


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