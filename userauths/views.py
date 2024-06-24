from django.shortcuts import render , redirect
from userauths.forms import User_Register_Form 
from django.contrib.auth import authenticate , login ,logout
from django.contrib import messages
from django.conf import settings
from .models import User
from django.http import HttpResponse
def register_view (request):
    if request.method=="POST" :
        form = User_Register_Form (request.POST) 
        if form.is_valid():
            new_user = form.save(commit=False)
            username= new_user.username
            email = new_user.email
            password = form.cleaned_data.get("password")
            new_user.set_password(password) 
            new_user.save()
            messages.success (request,f"Hi {username} Your account created Successfully")
            user_authenticate = authenticate(username=email,password=password)
            if user_authenticate is not None : 
                login(request,user_authenticate)
                return redirect("core:main")
            else :
                messages.error(request, "Error in Registration")
                return redirect ("userauths:sign-up")
    else : 
        form = User_Register_Form() 
            
    context = {
        'Register_form' : form 
    }
    return render (request,"userauths/sign-up.html",context)

def login_view (request):
    if request.user.is_authenticated:
        return redirect("core:main") 
    if request.method =="POST" :
        email = request.POST.get("email")
        password=request.POST.get("password") 
            #user= User.objects.get(email=email) #here catching Right User From Database Particuler Userauths.user Model 
        user = authenticate(request , email=email , password=password)  
        if user != None:
            login(request,user)
            messages.success(request,"You are Loged in")
            return redirect ("core:main")
        else :
            messages.warning(request," Wrong with Email Or password ")

       
   
    return render(request,"userauths/login.html",{})
def logout_view (request):
    logout(request)
    return redirect("userauths:log-in")


def hide_error_messages(request):
    return HttpResponse("")
def clear_error_message(request):
    global first_name
    print(first_name)
    if first_name==None or not (first_name==""):
            print(first_name)
            return HttpResponse("ffffffffff")
    else:
        return HttpResponse("")

      
    
    
            

        