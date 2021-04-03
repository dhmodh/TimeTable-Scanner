from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError, transaction
from django.contrib import messages
from django.http import HttpResponse

from .models import ScanTimeTableModel, UserCreationModel, SubjectFaculty
from .DataExtractor import Extractor
from .forms import UserForm, ScanTimeTableForm, SearchForm, SigninForm
from django.utils import timezone
import csv

# Create your views here.

def contactPage(request):
    return render(request, 'contactPage.html', {})

def aboutUs(request):
    return render(request, 'aboutUs.html', {})

def homePage(request):
    return render(request, 'home.html', {})

def loginPage(request):
    context={}

    if request.method == 'POST':
        form = SigninForm(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You login as "+user.username)
                return render(request, 'home.html', {})
                
            else:
                messages.error(request, 'Invalid Username or Password')

    else:
        form = SigninForm()
        
    context['form']=form

    return render(request, 'login.html', context)

def registrationPage(request):
    context={}

    if request.method == 'POST':
        form = UserForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.clean_password2()
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            name = form.cleaned_data['shortname']

            if User.objects.filter(username=username).exists() or User.objects.filter(password=password).exists():
                messages.error(request, 'Either Username or Password Match.\nUse other Username or Password.')

            else:
                try:
                    with transaction.atomic():
                        user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname, email=email, last_login = timezone.now())
                        userdata = UserCreationModel(user=user, name=name)
                        userdata.save()

                except DatabaseError:
                    transaction.rollback()

                messages.success(request, 'Sucessfully Registered')
                return render(request, 'login.html', {'form': SigninForm()})

    else:
        form = UserForm()
        
    context['form']=form
    return render(request, 'register.html', context)

@login_required(login_url='loginPage')
def logoutPage(request):
    messages.success(request, 'Sucessfully Logout from '+request.user.username)
    logout(request)
    return redirect(reverse('homePage'))

@login_required(login_url='loginPage')
def scanTimeTable(request):
    context = {}

    if request.method == 'POST':
        print('entered')
        form = ScanTimeTableForm(request.POST, request.FILES)

        if form.is_valid():
            tt = ScanTimeTableModel()
            tt.division = form.cleaned_data['division']
            tt.semester = form.cleaned_data['semester']
            tt.year = form.cleaned_data['year']
            tt.image = form.cleaned_data['image']

            sample = ScanTimeTableModel.objects.filter(division=tt.division, semester=tt.semester, year=tt.year).exists()

            if sample:
                messages.error(request, 'Time Table already Submitted.')

            else:
                tt.save()

                ttdata = Extractor(tt.image)
                ttdata.convertToGray()
                ttdata.grapStruct()
                ttdata.detectBoxAndExtract()

                data = ttdata.getData()
                request.session['data']=data

                try:
                    with transaction.atomic():
                        for d in data:
                            obj = SubjectFaculty(faculty=d[2], batch=d[1], subject=d[0], timetable=tt)
                            obj.save()
                except DatabaseError:
                    transaction.rollback()

                request.session['data'] = {'year':tt.year, 'division':tt.division, 'semester':tt.semester}
                return render(request, 'ttdata.html', {'data': data, 'tt':tt})

    else:
        form = ScanTimeTableForm()
        
    context['form']=form
    return render(request, 'timetable.html', context)

@login_required(login_url='loginPage')
def searchData(request):
    context={}

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            print("DMX")
            catagory = form.cleaned_data['catagory']
            content = form.cleaned_data['content']
            data= 0

            if catagory=='1':
                data = SubjectFaculty.objects.select_related('timetable').filter(faculty=content)
                data = data.order_by('timetable__year').reverse()

            elif catagory=='2':
                data = SubjectFaculty.objects.select_related('timetable').filter(timetable__division=content)
                data = data.order_by('timetable__year', 'subject').reverse()

            elif catagory=='3':
                data = SubjectFaculty.objects.select_related('timetable').filter(timetable__year=int(content))
                data = data.order_by('timetable__year', 'subject').reverse()
                
            else:
                data = SubjectFaculty.objects.select_related('timetable').filter(subject=content)
                data = data.order_by('timetable__year').reverse()

            context['data']=data

    else:
        form = SearchForm()
        
    context['form']=form
    return render(request, 'searchdata.html', context)

@login_required(login_url='loginPage')
def displayUserData(request):
    
    context = {}
    usershort = UserCreationModel.objects.filter(user=request.user)[0]
    data = SubjectFaculty.objects.select_related('timetable').filter(faculty=usershort).order_by('timetable__year').reverse()
    context['data']=data

    return render(request, 'userdata.html', context)


def loginPage(request):
    context={}

    if request.method == 'POST':
        form = SigninForm(request=request, data=request.POST)

        if form.is_valid():
            user = form.clean()

            if user is not None:
                login(request, form.user_cache)
                messages.success(request, "You login as "+user['username'])
                return render(request, 'home.html',{})
                
            else:
                messages.error(request, 'Invalid Username or Password')

    else:
        form = SigninForm()
        
    context['form']=form
    return render(request, 'login.html', context)
