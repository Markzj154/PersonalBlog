from django.urls import path
from blog.views import *

urlpatterns = [
	path('', blog_list, name='blog_list'),
    path('<int:blog_id>/', blog_detail, name='blog_detail'),
    path('type/<int:blog_type_id>/', blogs_with_type, name='blogs_with_type'),
    path('date/<int:year>/<int:month>/', blogs_with_date, name='blogs_with_date'),

]