from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import cv2
import numpy as np
import json
import base64
import openpyxl
from . models import student_data, mutiple_image_upload
import os
import math

#internal
def savedata(request):
    wrkbk = openpyxl.load_workbook("media\imp\student_data.xlsx")
    sh = wrkbk.active
    for row in sh.iter_rows(min_row=2, min_col=1, max_row=221, max_col=4):
        x=[]
        for cell in row:
            x.append(cell.value)
        data = student_data(stud_prn = x[0],stud_name = x[1], stud_div = x[2],stud_email = x[3])
        data.save()
    return HttpResponseRedirect("/")


def header(request):
    return render(request, "header.html")



def get_img(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_from_post = json.load(request)['post_data']
        img = cv2.imdecode(np.fromstring(base64.b64decode(data_from_post), dtype=np.uint8),cv2.IMREAD_UNCHANGED)

        #main processing
        haarCascade_face = cv2.CascadeClassifier("media/imp/haarcascade_frontalface_default.xml")
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.read('media/imp/face_trained.yml')

        gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        #detecting face
        faces_rect = haarCascade_face.detectMultiScale(gray_img,scaleFactor=1.1,minNeighbors = 4)
        for x,y,w,h in faces_rect:
            face_roi = gray_img[y:y+h,x:x+w]
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            label,confidence = face_recognizer.predict(face_roi) #lower the confidence, higher the similarity
     
            cv2.putText(img,str(label),(x,y),cv2.FONT_ITALIC,0.5,(0,255,255),2)
            cv2.putText(img,f'Error: {math.floor(confidence)}',(x,y+20),cv2.FONT_ITALIC,0.5,(0,200,255),2)

    
        #################

        img = cv2.imencode('.jpg', img)
        b64_string = base64.b64encode(img[1]).decode('utf-8')
        data = {
                'my_data':"data:image/png;base64,"+ b64_string
            }
        return JsonResponse(data)


def login_form(request):
    return render(request, "login_form.html",{})
    
def login_form_validate(request):
    prn = request.POST['stud_prn']
    return HttpResponseRedirect(f'/face_train/{prn}')
    
def face_train(request,prn):
    return render(request,"face_img_form.html",{"prn":prn})

def face_train_save_img(request,prn):
    all_images = request.FILES.getlist('stud_images')
    stud_data = student_data.objects.get(stud_prn=prn)
    for each_image in all_images:    
        img_data = mutiple_image_upload(train_input_reference=stud_data,train_images=each_image)
        img_data.save()
    return HttpResponseRedirect('/')



def home(request):
    return render(request, "home.html")

def dev(request):
    return render(request, "dev.html")

def train(request):
    dir = r'media\train'
    haarCascade_face = cv2.CascadeClassifier("media\imp\haarcascade_frontalface_default.xml")
    features = []
    lables = [] 

    for i in os.listdir(dir):
        for j in os.listdir(os.path.join(dir,i)):
            path = os.path.join(dir,i,j)
            label = int(j[-6:])
            for img_name in os.listdir(path): 
                img_path = os.path.join(path,img_name) 
                img = cv2.imread(img_path)
                gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                faces_rect = haarCascade_face.detectMultiScale(gray_img,scaleFactor=1.1,minNeighbors = 4)
                for x,y,w,h in faces_rect:
                    face_roi = gray_img[y:y+h,x:x+w] 
                    features.append(face_roi)
                    lables.append(label)
          
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    features = np.array(features,dtype='object')
    lables = np.array(lables)
    face_recognizer.train(features,lables)

    face_recognizer.save('media/imp/face_trained.yml')
    return HttpResponse("/")



