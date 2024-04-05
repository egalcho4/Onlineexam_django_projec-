from django.urls import path
from . import views
from studentbase import views as viw
from django.contrib.auth.views import LoginView
app_name="student"
urlpatterns = [
path('studentlogin', views.studentclick_view),
path('', LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
path('studentsignup', views.student_signup_view,name='studentsignup'),
path('student-dashboard/', views.student_dashboard_view,name='student-dashboard'),
path('student-exam', views.student_exam_view,name='student-exam'),
path('take-exam/<int:pk>', views.take_exam_view,name='take-exam'),
path('start-exam/<int:pk>', views.start_exam_view,name='start-exam'),

path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
path('view-result', views.view_result_view,name='view-result'),
path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('student-marks', views.student_marks_view,name='student-marks'),
#path('scan/',views.scan, name="scan"),
 path('livestraming/<token>',views.livestraming,name="livestraming"),
 path('livestram/',views.livestram,name="livestram"),
 path('cheating/',views.cheating,name="cheating"),
 #path('livestramface/',views.livestramface,name="livestramface"),
 path('st_message/',views.st_message,name="st_message"),

    path('start_random/<int:id>',views.start_random_exam,name="start_random"),
    path('profile_change/',views.profile_change,name="profile_change"),
    path('change_password/',views.change_password,name="change_password"),
    path('loby', views.lobby),
    path('room/', views.room,name="room"),
    path('get_token/', views.getToken),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
    path('registration/',views.registration,name="registration"),
    path('ask_for_help/',views.ask_for_help,name="ask_for_help"),
    path('sent_sms/',views.sent_sms,name="sent_sms"),
    path('sms_delete/<int:id>',views.sms_delete,name="sms_delete"),
    path('vdostremin/',views.vdostremin,name="vdostremin"),
    path('livestraminga/',views.livestraminga,name="livestraminga"),
    path('asiment/',views.asiment,name="asiment"),
]