from django.shortcuts import render
from django.http import JsonResponse
import cv2
import numpy as np
import json
import base64

def header(request):
    return render(request, "header.html")

def home(request):
    return render(request, "home.html")

def get_img(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_from_post = json.load(request)['post_data']
        img = cv2.imdecode(np.fromstring(base64.b64decode(data_from_post), dtype=np.uint8),cv2.IMREAD_UNCHANGED)

        #main processing
        gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        haarCascade_face = cv2.CascadeClassifier("reviewapp/haarcascade_frontalface_default.xml")
            
        faces_rect = haarCascade_face.detectMultiScale(gray_img,scaleFactor=1.1,minNeighbors = 4)
        for x,y,w,h in faces_rect:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),1)
  
        # ###############

        img = cv2.imencode('.jpg', img)
        b64_string = base64.b64encode(img[1]).decode('utf-8')
        data = {
                'my_data':"data:image/png;base64,"+ b64_string
            }
        return JsonResponse(data)


