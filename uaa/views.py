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
from django.conf import settings

from PIL import Image
import cv2
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from time import time
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import pickle

from home.views import send_sms

BASE_DIR = settings.BASE_DIR
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
#   try:  
    if request.method=='POST':
        
        first_name = request.POST.get('name')
        first,last= first_name.split(' ')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        group_id = request.POST.get('group')
        num = random.randint(10,9999) 
        username= f'{str(first).lower()}{num}'
        password = make_password('sijura123')
     
        phones = phone[1:]
        #print(phones)
    
      
        group = Group.objects.get(id=group_id)
        user=User.objects.filter(username=username).exists()
       
        if user:
            messages.error(request,'username exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            u = User.objects.create(first_name=first_name,email=email,last_name=phone,username=username,password=password)
            id = User.objects.get(username=u)
            id = id.id
            # print(l.id)
            # print(u)
            u.groups.add(group)
            faceDetect = cv2.CascadeClassifier(BASE_DIR+'/ml/haarcascade_frontalface_default.xml')
            cam = cv2.VideoCapture(0)
            id = id
            sampleNum = 0
            
            while(True):
               ret, img = cam.read()
               gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
               faces = faceDetect.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3, minSize=(30, 30), maxSize=(300, 300))
               
               for(x,y,w,h) in faces:
                  sampleNum = sampleNum+1
                  cv2.imwrite(BASE_DIR+'/ml/dataset/user.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])
                  
                  cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
                  cv2.waitKey(250)
               cv2.imshow("Face",img)
               cv2.waitKey(1)
               if(sampleNum>35):
                  break
            
            
            cam.release()
    # destroying all the windows
            cv2.destroyAllWindows()
            # body = "🏨 WELCOME TO SIJURA LODGE 🏨 \n🙏 THANKS FOR BOOKING ROOM NO.🛌 \n🔑 YOUR CONFIRMATION CODE IS🔑  \n⚠️ keep safe the confirmation code for your booking as it will be used later⚠️ \n🙏THANK YOU AND WELCOME AGAIN 😊"
            message = f'{first_name} \nWELCOME TO SIJURA LODGE\nUsername: {username}\nPassword: {username}'
            #p = send_sms(phones,message)
            #print(p)
            messages.success(request,'user added successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    g = Group.objects.all()
    user = User.objects.all()
    
    context = {'g':g,'user':user}
    return render(request,'users.html',context)
#   except Exception as e:
#         messages.success(request,e)
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    
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
 

 
 
# def create_dataset(request):
#     #print request.POST
#     userId = int(request.POST['userId'])
    
#     status = False
#     for i in data:
#         for j,k in i.items():
#             if j == 'reg_number' and k == userId:
#                status = True
#                print('ok')
#                Records.objects.create(id=userId,first_name=i['first_name'],last_name=i['last_name'],registration_status=i['status'],course=i['course'],className=i['className'],year_of_study=i['year_of_study'])
#     if not status:
#         messages.error(request, 'Registration number does not exist')
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#     print (cv2.__version__)
#     # Detect face
#     #Creating a cascade image classifier
#     faceDetect = cv2.CascadeClassifier(BASE_DIR+'/ml/haarcascade_frontalface_default.xml')
#     #camture images from the webcam and process and detect the face
#     # takes video capture id, for webcam most of the time its 0.
#     cam = cv2.VideoCapture(0)

#     # Our identifier
#     # We will put the id here and we will store the id with a face, so that later we can identify whose face it is
#     id = userId
#     # Our dataset naming counter
#     sampleNum = 0
#     # Capturing the faces one by one and detect the faces and showing it on the window
#     while(True):
#         # Capturing the image
#         #cam.read will return the status variable and the captured colored image
#         ret, img = cam.read()
#         #the returned img is a colored image but for the classifier to work we need a greyscale image
#         #to convert
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         #To store the faces
#         #This will detect all the images in the current frame, and it will return the coordinates of the faces
#         #Takes in image and some other parameter for accurate result
#         faces = faceDetect.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3, minSize=(30, 30), maxSize=(300, 300))

#         #In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.
#         for(x,y,w,h) in faces:
#             # Whenever the program captures the face, we will write that is a folder
#             # Before capturing the face, we need to tell the script whose face it is
#             # For that we will need an identifier, here we call it id
#             # So now we captured a face, we need to write it in a file
#             sampleNum = sampleNum+1
#             # Saving the image dataset, but only the face part, cropping the rest
#             cv2.imwrite(BASE_DIR+'/ml/dataset/user.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])
#             # @params the initial point of the rectangle will be x,y and
#             # @params end point will be x+width and y+height
#             # @params along with color of the rectangle
#             # @params thickness of the rectangle
#             cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
#             # Before continuing to the next loop, I want to give it a little pause
#             # waitKey of 100 millisecond
#             cv2.waitKey(250)

#         #Showing the image in another window
#         #Creates a window with window name "Face" and with the image img
#         cv2.imshow("Face",img)
#         #Before closing it we need to give a wait command, otherwise the open cv wont work
#         # @params with the millisecond of delay 1
#         cv2.waitKey(1)
#         #To get out of the loop
#         if(sampleNum>35):
#             break
#     #releasing the cam
#     cam.release()
#     # destroying all the windows
#     cv2.destroyAllWindows()

#     return redirect('/')



def trainer(request):
    '''
        In trainer.py we have to get all the samples from the dataset folder,
        for the trainer to recognize which id number is for which face.

        for that we need to extract all the relative path
        i.e. dataset/user.1.1.jpg, dataset/user.1.2.jpg, dataset/user.1.3.jpg
        for this python has a library called os
    '''
    import os
    from PIL import Image

    #Creating a recognizer to train
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #Path of the samples
    path = BASE_DIR+'/ml/dataset'

    # To get all the images, we need corresponing id
    def getImagesWithID(path, img_size=(128, 128)):
        # create a list for the path for all the images that is available in the folder
        # from the path(dataset folder) this is listing all the directories and it is fetching the directories from each and every pictures
        # And putting them in 'f' and join method is appending the f(file name) to the path with the '/'
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)] #concatinate the path with the image name
        #print imagePaths

        # Now, we loop all the images and store that userid and the face with different image list
        faces = []
        Ids = []
        for imagePath in imagePaths:
            # First we have to open the image then we have to convert it into numpy array
            faceImg = Image.open(imagePath).convert('L') #convert it to grayscale
            # converting the PIL image to numpy array
            # @params takes image and convertion format
            faceNp = cv2.resize(np.array(faceImg), img_size)
            # Now we need to get the user id, which we can get from the name of the picture
            # for this we have to slit the path() i.e dataset/user.1.7.jpg with path splitter and then get the second part only i.e. user.1.7.jpg
            # Then we split the second part with . splitter
            # Initially in string format so hance have to convert into int format
            ID = int(os.path.split(imagePath)[-1].split('.')[1]) # -1 so that it will count from backwards and slipt the second index of the '.' Hence id
           
            
            # Images
            faces.append(faceNp)
            # Label
            Ids.append(ID)
            #print ID

           
            cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return np.array(Ids), np.array(faces)

    # Fetching ids and faces
    ids, faces = getImagesWithID(path)
    #Training the recognizer
    # For that we need face samples and corresponding labels
    recognizer.train(faces, ids)

    # Save the recogzier state so that we can access it later
    recognizer.save(BASE_DIR+'/ml/recognizer/trainingData.yml')
    cv2.destroyAllWindows()

    messages.success(request,'Train Successful')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def loginWithFace(request):
 try:
    if request.method == 'POST':
     
      email=request.POST.get("email")
      password='sijura123'
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
 
def detect(request):
   
   
   
      
    
    password='sijura123'
    
      
    faceDetect = cv2.CascadeClassifier(BASE_DIR+'/ml/haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)
    # creating recognizer
    rec = cv2.face.LBPHFaceRecognizer_create()
    # loading the training data
    rec.read(BASE_DIR+'/ml/recognizer/trainingData.yml')
    getId = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    userId = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3, minSize=(30, 30), maxSize=(300, 300))
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)

            getId,conf = rec.predict(gray[y:y+h, x:x+w]) #This will predict the id of the face
            print(getId)
            #print conf;
            if conf<65:
                userId = getId
                
                cv2.putText(img, "Detected",(x,y+h), font, 2, (0,255,0),2)
                
            else:
                cv2.putText(img, "Unknown",(x,y+h), font, 2, (0,0,255),2)

            # Printing that number below the face
            # @Prams cam image, id, location,font style, color, stroke

        cv2.imshow("Face",img)
        if(cv2.waitKey(1) == ord('q')):
            break
        elif(userId != 0):
            u = User.objects.get(id=userId)
            
            user = auth.authenticate(request, username=u.username, password=password)
            if user is not None:
             auth.login(request,user)
             cv2.waitKey(1000)
             cam.release()
             cv2.destroyAllWindows()
             return redirect('/admins')
            else:
             messages.error(request,'user not recoginized')
             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return redirect('/records/details/'+ str(userId))

    cam.release()
    cv2.destroyAllWindows()
    return redirect('/')
   