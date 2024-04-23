from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


# Create your views here.

@login_required(login_url='login')
def Homepage(request):
    return render(request,'home.html')


def Signuppage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if pass1!=pass2:
            return HttpResponse("your enter password and confirm password are not matched")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.is_active = False  # Deactivate the user initially
            my_user.save()
            send_verification_email(my_user)
            return HttpResponse("A verification email has been sent to your email address. Please verify your email to activate your account.")

           
            
            '''return HttpResponse("User account created successfully...")
            print(uname,email,pass1,pass2)
'''
    return render(request,'signup.html')


def send_verification_email(user):
    subject = 'Verify your email'
    message = f'Hi {user.username},\n\nClick the link below to verify your email:\n\nhttp://yourdomain.com/verify/{user.id}/'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)
    return redirect('login')


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        send_verification_email(instance)


def verify_email(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, 'Your email has been verified. You can now log in.')
    return redirect('login')


def Loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        print(username,pass1)
        user=authenticate(request,username=username,password=pass1)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("username or password is wrong")


    return render(request,'login.html')



def Logout(request):
    logout(request)
    return redirect('login')