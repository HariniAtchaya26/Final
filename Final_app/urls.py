from django.urls import path
from .views import student_list, add_student_post

urlpatterns = [
    path("students/", student_list),
    path("add-student/", add_student_post),
]
