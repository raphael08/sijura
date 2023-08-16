import random
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import *
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User,auth,Permission,Group
from django.contrib.auth.decorators import *
from django.contrib.auth.hashers import make_password

from home.views import send_sms


def login(request):
 try:
    if request.method == 'POST':
     
      email=request.POST.get("email")
      password=request.POST.get("password")
      print(email,password)
      user = auth.authenticate(request, username=email, password=password)
      if user is not None:
        auth.login(request,user)
        messages.success(request,'Login successful')
        return redirect('/admins')
      else:
        messages.error(request,'Password Or Username is wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request,'login.html')
 except:
     messages.error(request,'something is wrong')
     return redirect('uaa/')    
 
@login_required(login_url='/uaa/') 
def logout(request):
    
    auth.logout(request)
    messages.success(request,'logout successful')
    return redirect('/uaa/') 

@login_required(login_url='/uaa/') 
def adduser(request):
  try:  
    if request.method=='POST':
        
        first_name = request.POST.get('name')
        first,last= first_name.split(' ')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        group_id = request.POST.get('group')
        num = random.randint(10,9999) 
        username= f'{str(first).lower()}{num}'
        password = make_password(username.lower())
     
        phones = phone[1:]
        print(phones)
    
      
        group = Group.objects.get(id=group_id)
        user=User.objects.filter(username=username).exists()
        if user:
            messages.error(request,'username exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            u = User.objects.create(first_name=first_name,email=email,last_name=phone,username=username,password=password)
            u.groups.add(group)
            # body = "🏨 WELCOME TO SIJURA LODGE 🏨 \n🙏 THANKS FOR BOOKING ROOM NO.🛌 \n🔑 YOUR CONFIRMATION CODE IS🔑  \n⚠️ keep safe the confirmation code for your booking as it will be used later⚠️ \n🙏THANK YOU AND WELCOME AGAIN 😊"
            message = f'{first_name} \nWELCOME TO SIJURA LODGE\nUsername: {username}\nPassword: {username}'
            p = send_sms(phones,message)
            print(p)
            # messages.success(request,'user added successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    g = Group.objects.all()
    user = User.objects.all()
    
    context = {'g':g,'user':user}
    return render(request,'users.html',context)
  except Exception as e:
        messages.success(request,e)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    
@login_required(login_url='/uaa/')     
def editUser(request,id):
 try:
   if request.method=="POST":
    firstname = request.POST.get("name")
    lastname = request.POST.get("phone")
    email = request.POST.get("email")
    username = request.POST.get("username")
    group_id = request.POST.get('group')
      
    group = Group.objects.get(id=group_id)
    User.objects.filter(id=id).update(first_name=firstname,last_name=lastname,email=email,username=username)
    u = User.objects.get(id=id)
    for i in Group.objects.all():
            u.groups.remove(i.id)
    u.groups.add(group)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
 except Exception as e:
    messages.success(request,e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


@login_required(login_url='/uaa/') 
def deleteUser(request,id):
 try: 
    User.objects.filter(id=id).delete()
    messages.error(request,'successful')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
 except Exception as e:
    messages.error(request,e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 



@login_required(login_url='login/')
def addroles(request):
  try:
   p = Group()
   if request.method == "POST":
      name = request.POST.get("name")
      permission = [x.name for x in Permission.objects.all()]
      s_id = []
      p.name=name
      for x in permission:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      p.save()
      for s in s_id:
           p.permissions.add(Permission.objects.get(id=s))   
      messages.success(request,'Role added successful')
      return redirect('/manageroles')  
  except:
      
    messages.error(request,'Something went wrong')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url='/uaa/')
def editroles(request,pk):
   
  try:
   exclude_perm=[1]
   p = Permission.objects.exclude(id__in=exclude_perm)
   r = Group.objects.filter(id=pk)
   y=Group.objects.get(id=pk)
   if request.method == 'POST':
    name = request.POST.get('name')
    
             
    for j in Permission.objects.all():
              y.permissions.remove(j.id) 
      
      
    permission = [x.name for x in Permission.objects.all()]
     
    s_id = []
    Group.objects.filter(id=pk)
    for x in permission:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
    r=Group.objects.filter(id=pk).update(name=name)
      
    for s in s_id:
           y.permissions.add(Permission.objects.get(id=s))  
    messages.success(request,'Login successful')
    return redirect('/manageroles')
           
   return render(request,'html/dist/editroles.html',{'r':r,'p':p})
  except:
      messages.error(request,'Something is wrong')


@login_required(login_url='login/')
def manageroles(request):
   try: 
      g = Group.objects.all().order_by('id')
      exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24]
      p = Permission.objects.exclude(id__in=exclude_perm)
      
      return render(request,'html/dist/manageroles.html',{'side':'role','p':p,'g':g})
   except:
    messages.error(request,'Something went wrong')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/uaa/')     
def blockuser(request,pk):
       
     
      try:
         u = User.objects.filter(id=pk).filter(is_active='True')
         if u:      
            User.objects.filter(id=pk).update(is_active='False')
            messages.success(request,'block successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
         else:
            User.objects.filter(id=pk).update(is_active='True') 
            messages.success(request,'Activation successful') 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      except: 
       messages.error(request,'Something went Wrong')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/uaa/')     
def unblockuser(request,pk):
       
     
      try:
         u = User.objects.filter(id=pk).filter(is_active='False')
         if u:      
            User.objects.filter(id=pk).update(is_active='True')
            messages.success(request,'Unblock successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
         else:
            User.objects.filter(id=pk).update(is_active='False') 
            messages.success(request,'Activation successful') 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      except: 
       messages.error(request,'Something went Wrong')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/uaa/')   
def deleteroles(request,pk):
   try: 
    g = Group.objects.filter(id=pk).delete()
    if g:
       messages.success(request,'Role deleted successful')
    
    return redirect('/manageroles')
   except:
    messages.error(request,'Something went wrong')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='/uaa/')
def reset_password(request,pk):
   password = make_password("sijura123")
   User.objects.filter(id=pk).update(password=password)
   messages.success(request,'Password reseted successful')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/uaa/')
def changepassword(request):
 try:
   if request.method =='POST':
      old = request.POST.get("old")
      new = request.POST.get("new")
      comf = request.POST.get("comf")
      # print(request.user.check_password(old))
      if (request.user.check_password(old)):
       if (new == comf): 
         User.objects.filter(username=request.user.username).update(password=make_password(new))
         messages.success(request,'successful password changed login again')
         return redirect('/uaa/')
       else:
           messages.error(request,'Password Dont Match')
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      else:
         messages.error(request,'Check Your Old Password')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 except:
    messages.error(request,'Something went wrong')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))