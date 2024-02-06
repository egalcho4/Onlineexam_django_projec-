from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView
app_name="teacher"
urlpatterns = [
path('teacherclick', views.teacherclick_view),
path('', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teacherlogin/', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teachersignup', views.teacher_signup_view,name='teachersignup'),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),

path('qeditblanck/<int:id>',views.qeditblanck,name="qeditblanck"),
path('cqeditblanck/<int:id>',views.cqeditblanck,name="cqeditblanck"),
path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher_add_question/<int:id>', views.teacher_add_question_view,name='teacher_add_question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),
path('delet_test/<int:id>',views.delet_test,name="delet_test"),

path('teacher_manage_course/',views.teacher_manage_course,name="teacher_manage_course"),
path('qtdelete/<int:id>/',views.qtdelete,name="qtdelete"),
path(' teacher_wiew_course/',views.teacher_wiew_course,name="teacher_wiew_course"),
path('register_student_view/',views.register_student_view,name="register_student_view"),
path('teacher_add_student/<int:sem>',views.teacher_add_student,name="teacher_add_student"),
path('delete_student/<int:id>',views.delete_student,name="delete_student"),
path('student_marks/',views.student_marks,name="student_marks"),
path('exam_schedule/<int:id>',views.exam_schedule,name="exam_schedule"),
path('update-student/<int:pk>', views.update_student_view,name='update-student'),
path('livestreaming/',views.livestreaming,name="livestreaming"),
path('assgine_lecturer/<int:id>',views.assgine_lecturer,name="assgine_lecturer"),
path('settings/',views.settings,name="settings"),
path('enable_student/<int:id>',views.enable_student,name="enable_student"),
path('disable_student/<int:id>',views.disable_student,name="disable_student"),
path('qedit/<int:id>',views.qedit,name="qedit"),
path('control_exam_status/<int:id>',views.control_exam_status,name="control_exam_status"),
path('sendmsg',views.sendmsg,name="sendmsg"),
path('delete_courses/<int:id>',views.delete_courses,name="delete_courses"),
path('see_message/<int:id>',views.see_message,name="see_message"),
path('first_exam/<int:id>',views.first_exam,name="first_exam"),

path('report/<int:id>',views.report,name="report"),
path('control_exam/',views.control_exam,name="control_exam"),
path('loby', views.lobby,name="loby"),
path('room/', views.room,name="room"),
path('get_token/', views.getToken),

path('create_member/', views.createMember),
path('get_member/', views.getMember),
path('delete_member/', views.deleteMember),
path('msgsender/',views.msgsender,name="msgsender"),
path('notfication/',views.notfication,name="notfication"),
path('seen_not',views.seen_not,name="seen_not"),
path('not_repl/<int:id>',views.not_repl,name="not_repl"),
path('start_all_exam/',views.start_all_exam,name="start_all_exam"),
path('start_now/<int:id>',views.start_now,name="start_now"),
path('stop_now/<int:id>',views.stop_now,name="stop_now"),
path('show_answer_now/<int:id>',views.show_answer_now,name="show_answer_now"),
path('dont_show_answer_now/<int:id>',views.dont_show_answer_now,name="dont_show_answer_now"),
path('student_mark_report/<int:id>',views.student_mark_report,name="student_mark_report"),
path('blanck_question/',views.blanck_question,name="blanck_question"),
path('short_question/',views.short_question,name="short_question"),
path('true_false_question/',views.true_false_question,name="true_false_question"),
path('paragraph/',views.paragraph,name="paragraph"),
path('register_student_view_code/',views.register_student_view_code,name="register_student_view_code"),
path('enable_student_code/<int:id>',views.enable_student_code,name="enable_student_code"),
path('account_update/',views.account_update,name="account_update"),
path('change_password/',views.change_password,name="change_password"),
path('see_exam_detail/<int:id>',views.see_exam_detail,name="see_exam_detail"),
 path('add_year/',views.add_year,name="add_year"),  
 path('add_table/',views.add_tabele,name="add_tabele"),
 path('image_upadeta/',views.image_upadeta,name="image_upadeta"),
 path('wwitout_image/',views.wwitout_image,name="wwitout_image"),
 path('makepretest/<int:id>',views.makepretest,name="makepretest"),
 path('exam_password_set',views.exam_password_set,name="exam_password_set"),
 path('asissment/',views.asissment,name="asissment"),
 path('ipadress/',views.ipadress,name="ipadress"),
 path('removeipfrom/',views.removeipfrom,name="removeipfrom"),

]