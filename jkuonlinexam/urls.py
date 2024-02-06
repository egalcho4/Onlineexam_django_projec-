

from django.urls import path,include
from django.contrib import admin
from exam import views
from django.contrib.auth.views import LogoutView,LoginView
from django.conf import settings
#from django.conf.urls import url
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
     
     
    
     path('depart/',include('teacher.urls',namespace="teacher")),
    path('student/',include('student.urls',namespace="student")),
    path('',include('exam.urls',namespace="exam")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

