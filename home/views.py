from django.shortcuts import render,redirect
from django.http import HttpResponse

from .forms import BookingForm, RegisterForm

from .models import Departments,Doctors
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    numbers ={
        'fruits':["banana","mango"]
    }
    return render(request,'index.html',numbers)

def about(request):
    return render(request,'about.html')

@login_required
def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
           booking = form.save(commit=False)
           booking.user = request.user
           booking.save()
           return render(request, 'confirmation.html')
    form = BookingForm()
    dict_form={
        'form':form
    }
    return render(request, 'booking.html', dict_form)

def doctors(request):
    dict_docs={
        'doctors': Doctors.objects.all()
    }
    return render(request,'doctors.html',dict_docs)

def contact(request):
    return render(request,'contact.html')

def department(request):
    dict_dept={
        'dept' : Departments.objects.all()
    }
    return render(request,'department.html',dict_dept)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
           login(request, user)

           next_url = request.GET.get('next')

           if next_url:
               return redirect(next_url)
           else:
               return redirect('/')

        else:
          return render(request, "login.html", {
            "error": "Invalid username or password. If you don't have an account, please register first."
          })

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})