from django.urls import path
from myapp import views
app_name = 'myapp'
urlpatterns = [
 path(r'', views.index, name='index'),
 path(r'<int:top_no>/', views.detail, name='detail'),
 path(r'about/', views.about, name='about'),
 path(r'courses/', views.courses, name='courses'),
 path(r'courses/<int:cour_id>', views.coursedetail, name='course_detail'),
 path(r'coursedetail/<int:cour_id>', views.coursedetail, name='Course Details'),
 path(r'place_order/', views.place_order, name='place order'),
 path(r'login/', views.user_login, name='login'),
 path(r'logout/', views.user_logout, name='logout'),
 path(r'myaccount/', views.myaccount, name='myaccount'),
]
