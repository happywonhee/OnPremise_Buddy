from django.shortcuts import render

# Create your views here.

def Detail1(request):
    return render(request,'stay/detail1.html')

def Detail2(request):
    return render(request,'stay/detail2.html')

def Detail3(request):
    return render(request,'stay/detail3.html')

def Stay(request):
    return render(request,'stay/stay.html')