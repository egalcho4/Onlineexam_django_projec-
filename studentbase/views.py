
from django.shortcuts import render
from django.http import JsonResponse
import random
import time
#from agora_token_builder import RtcTokenBuilder
#from base.models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.db.models import Q
from django.views.decorators import gzip
import cv2
import time
import base64
import threading
from student import models as SModel
import time
from django.contrib.auth.models import User
from datetime import date, timedelta
from datetime import datetime
import cv2,pandas
import numpy as np
import os


"""# Create your views here.

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')


def getToken(request):
    appId = "c7d8770db57247ff99b35f234fb77e4e"
    appCertificate = "edd4527ce66941dcb2850092ad69045c"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)"""
class VideoCamera(object):
    id=""
    name=""
    course=""
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
       
        

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
        
    
        
    def update(self):
        static_back = None
        motion_list = [ None, None ]
        time = []
        df = pandas.DataFrame(columns = ["Start", "End"])
        while True:
            (self.grabbed, self.frame) = self.video.read()
            motion = 0
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            if static_back is None:
                static_back = gray
                continue
            diff_frame = cv2.absdiff(static_back, gray)
            thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
            cnts,_ = cv2.findContours(thresh_frame.copy(), 
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in cnts:
                if cv2.contourArea(contour) < 10000:
                    continue
                motion += 1
              
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            motion_list.append(motion)
  
            motion_list = motion_list[-2:]
            if motion_list[-1] == 1 and motion_list[-2] == 0:
              time.append(datetime.now())
              
              
            if motion_list[-1] == 0 and motion_list[-2] == 1:
               time.append(datetime.now())
               mn=0
               if motion > 1:
                         mn+=1
                         ex=SModel.Exam_control(
                           name=self.name,
                           user_id=User.objects.get(pk=self.id),
                           mot_count=motion,
                           tyme=mn,
                           exam=self.course,
                       )
                         ex.save()
                    
                       
            

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livestram(request):
    
    try:
      cam = VideoCamera()
      cam.id=request.user.id
      cam.name=request.user
      cam.course= request.session['c_id']
      
      return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except: 
        pass
class LiveControl(object):
    id=""
    name=""
    course=""
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.updat, args=()).start()
        self.GET, self.POST, self.COOKIES, self.META, self.FILES = {}, {}, {}, {}, {}
        
    

    def __del__(self):
        self.video.release()

    def get_fram(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def updat(self):
       
       
        
       
       
       
        weight=os.path.abspath(os.getcwd()) +'\static\yolo\yolov3 .weights'
        
        config=os.path.abspath(os.getcwd()) +'\static\yolo\yolov3.cfg'
      
        
        net = cv2.dnn.readNet(weight, config)
        classes = []
        with open(os.path.abspath(os.getcwd()) +'\static\yolo\coco.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        outputlayers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        while True:
            (self.grabbed, self.frame) = self.video.read()
            
            
            
            img = cv2.resize(self.frame, None, fx=0.2, fy=0.2)
            height, width, channels = img.shape
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(outputlayers)
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            #print(indexes)
            font = cv2.FONT_HERSHEY_PLAIN
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    color = colors[class_ids[i]]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
                    
                    nm=0
                    if label=="laptop" or label=="cell phone" or label=="book" or label=="clock" or label=="remote":
                         
                         ex=SModel.Exam_control(
                           name=self.name,
                           user_id=User.objects.get(pk=self.id),
                           material=label,
                           tyme=nm,
                           exam=self.course,
                       )
                         ex.save()
                        
                                        
                    
                    
            

def gena(camera):
    while True:
        frame = camera.get_fram()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def cheating(request):
    
    try:
      cam = LiveControl()
      cam.id=request.user.id
      cam.name=request.user
      cam.course= request.session['c_id']
      return StreamingHttpResponse(gena(cam), content_type="multipart/x-mixed-replace;boundary=frame")
      
    except: 
        pass
