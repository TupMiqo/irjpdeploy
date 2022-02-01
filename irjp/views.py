from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .models import Registration
from .forms import RegistrationForm, CreateUserForm


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def teacher(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form.instance.is_superuser = True
        if form.is_valid():
            form.save()
            return redirect('login2')


    context = {
        'form': form
    }
    return render(request, 'T-register.html', context)


def home(request):
    return render(request, 'Home.html')
   
def Register(request):
    if request.user.is_authenticated:
        return redirect ('Home')
    else:
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()

        context = {
            'form': form
        }
        return render(request, 'Register.html', context)

def login2(request): 
    if request.user.is_authenticated and request.user.is_superuser: 
        return redirect ('table')
    else:
        if request.method == 'POST':
            userss = request.POST.get('username')
            passw = request.POST.get('password') 

            user = authenticate(request, username=userss,password=passw)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('table')
                
            else:
                messages.info(request,'Username/Password is incorrect')

        context = {}

        return render(request, 'T-login.html', context)
  

@login_required(login_url='login2')
def table(request):
    registration_data = Registration.objects.all()
    
    getdata = {
        'data': registration_data
    }
    return render(request, 'table.html', getdata)

@login_required(login_url='login2')
def edittable(request, data_id):
    student_data = Registration.objects.get(id=data_id)
    form = RegistrationForm(request.POST or None, instance=student_data)

    context = {
        "form": form,
        "student": student_data
        }
    
    if form.is_valid():
        form.save()
        return redirect('table')

    return render(request, 'edittable.html', context)

@login_required(login_url='login2')
def delete_data(request, data_id):
    student_info = Registration.objects.get(id=data_id)

    if request.method == "POST":
        student_info.delete()
        return redirect('table')


    return render(request, 'delete_data.html', {'student_info': student_info})
    


def logoutUser(request):
	logout(request)
	return redirect('login2')
