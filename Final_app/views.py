from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .services import get_students, create_student
from django.views.decorators.csrf import csrf_exempt
import json


async def student_list(request):
    students = await get_students()
    data = [{"id": s.id, "name": s.name} for s in students]
    return JsonResponse(data, safe=False)

async def add_student(request):
    name = request.GET.get("name")
    email = request.GET.get("email")

    student = await create_student(name, email)
    return JsonResponse({"id": student.id, "name": student.name})

@csrf_exempt
async def add_student_post(request):
    if request.method == "POST":
        body = json.loads(request.body)
        student = await create_student(
            body["name"],
            body["email"]
        )
        return JsonResponse({
            "id": student.id,
            "name": student.name
        })
