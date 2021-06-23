from django.shortcuts import redirect, render
from .forms import RegisterForm,LoginForm 
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

# Create your views here.

def registerUser(request):
    registerform=RegisterForm(request.POST or None)
    context = {
        "form1":registerform
         }
    if registerform.is_valid():
        username=registerform.cleaned_data.get("username")
        password = registerform.cleaned_data.get("password")
        newUser=User(username=username)
        newUser.set_password(password)
        newUser.save()
        login(request, newUser)
        messages.info(request,"Başarı ile kayıt oldunuz")    
        return redirect ("index")
    
    return render(request, "register.html", context)

    
    
""" Bu şekilde yapılabilir ancak daha da profesyonel yöntemi yukarıda 
    registerform=RegisterForm()
    content = {
        "form1":registerForm
         }
    if request.method=="POST":
        registerform=RegisterForm(request.POST)
        if registerform.is_valid():
            username=registerform.cleaned_data.get("username")
            password = registerform.cleaned_data.get("password")
            newUser=User(username=username)
            newUser.set_password(password)
            newUser.save()
            login(request, newUser)    
            return redirect ("index")
        else:
            return render(request, "register.html", content)
    else:
        return render(request, "register.html", content) """

    


def loginUser(request):
    loginform=LoginForm(request.POST or None)
    context = {
        "form2":loginform
         }
    if loginform.is_valid():
       username=loginform.cleaned_data.get("username")
       password = loginform.cleaned_data.get("password")
       user= authenticate(username=username, password=password)

       if user is None:
           messages.warning(request, "Kullanıcı Bilgileri yanlış")
           return render(request, "login.html", context)
       else:
           login(request, user)
           messages.info(request,"Başarı ile giriş yaptınız")    
           return redirect ("index")

    return render(request, "login.html", context)
    
def logoutUser(request):
    logout(request)
    messages.success(request, "Çıkış yapıldı")
    return redirect ("index")
