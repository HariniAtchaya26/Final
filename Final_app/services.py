from asgiref.sync import sync_to_async
from .models import Student

@sync_to_async
def get_students():
    return list(Student.objects.all())

@sync_to_async
def create_student(name, email):
    return Student.objects.create(name=name, email=email)
