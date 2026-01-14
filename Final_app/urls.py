from django.urls import path
from .views import (
    student_list, add_student_post,
    signup_view, login_view, logout_view, profile_view, profile_update, signup_form, login_form, profile_form

)

urlpatterns = [
    path("students/", student_list),
    path("add-student-post/", add_student_post),
    path("signup/", signup_view),
    path("login/", login_view),
    path("logout/", logout_view),
    path("profile/", profile_view),
    path("profile/update/", profile_update),
    path("signup-form/", signup_form),
    path("login-form/", login_form),
    path("profile-form/", profile_form),
]