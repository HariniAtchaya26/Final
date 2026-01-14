from asgiref.sync import sync_to_async

from .models import UserProfile
from .models import Student
from .models import Profile
from django.contrib.auth.models import User

@sync_to_async
def get_students():
    return list(Student.objects.all())

@sync_to_async
def create_student(name, email):
    return Student.objects.create(name=name, email=email)
@sync_to_async
def create_or_update_profile(user, phone, address, avatar=None):
    profile, _ = UserProfile.objects.update_or_create(
        user=user,
        defaults={
            "phone": phone,
            "address": address,
            "avatar": avatar
        }
    )
    return profile

@sync_to_async
def get_profile(user):
    return UserProfile.objects.get(user=user)
@sync_to_async
def get_or_create_profile(user):
    profile, created = Profile.objects.get_or_create(user=user)
    return profile

@sync_to_async
def update_profile(user, phone, address, avatar):
    profile, created = Profile.objects.get_or_create(user=user)
    profile.phone = phone
    profile.address = address
    profile.avatar = avatar
    profile.save()
    return profile