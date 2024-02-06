from django.test import TestCase

# Create your tests here.
"""class VFacedect(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.outoupdate, args=()).start()

    def __del__(self):
        self.video.release()

    def get_framface(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def outoupdate(self):
        request=self
        known_face_encodings = []
        known_face_names = []
        profiles = SModel.Student.objects.all()
        for profile in profiles:
            person = profile.profile_pic
            image_of_person = face_recognition.load_image_file(f'media/{person}')
        
    
            #person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
           
            person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
           
            
            known_face_encodings.append(person_face_encoding)
            known_face_names.append(f'{person}'[:-10])
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        while True:
            (self.grabbed, self.fram) = self.video.read()
            small_frame = cv2.resize(self.fram, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                        
                        
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    
                    if not matches[best_match_index]:
                        print("not")
                           
                    elif matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        print("yes") 
                       
                            
                            
                    else:
                        print("either") 
                          
                           
                    profile = SModel.Student.objects.get(Q(profile_pic__icontains=name))
                       # return JsonResponse({'not':1},status=200)
                 
                    face_names.append(name)
                    
            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(self.fram, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(self.fram, (left, bottom - 35),
                            (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.fram, name, (left + 6, bottom - 6),
                            font, 0.5, (255, 255, 255), 1)
            
def genface(camera):
    while True:
        frame = camera.get_framface()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livestramface(request):
    try:
      cam = VFacedect()
      return StreamingHttpResponse(genface(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except: 
        pass"""