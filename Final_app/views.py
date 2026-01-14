from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Profile
from django.shortcuts import render


from .services import (
    get_students,
    create_student,
    get_or_create_profile,
    update_profile
)

# ================= STUDENT APIs =================

async def student_list(request):
    students = await get_students()
    data = [{"id": s.id, "name": s.name} for s in students]
    return JsonResponse(data, safe=False)


@csrf_exempt
async def add_student_post(request):
    if request.method != "POST":
        return JsonResponse({"message": "Use POST method"}, status=405)

    try:
        body = json.loads(request.body)
        name = body.get("name")
        email = body.get("email")

        if not name or not email:
            return JsonResponse({"error": "name and email required"}, status=400)

        student = await create_student(name, email)
        return JsonResponse({"id": student.id, "name": student.name})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


# ================= AUTH HELPERS =================

@sync_to_async
def create_user(username, password):
    return User.objects.create_user(username=username, password=password)


@sync_to_async
def authenticate_user(username, password):
    return authenticate(username=username, password=password)


@sync_to_async
def login_user(request, user):
    login(request, user)


@sync_to_async
def logout_user(request):
    logout(request)


@sync_to_async
def get_or_create_user_profile(user):
    return Profile.objects.get_or_create(user=user)



# ================= AUTH APIs =================

@csrf_exempt
async def signup_view(request):
    if request.method != "POST":
        return JsonResponse({"message": "Use POST method for signup"}, status=405)

    try:
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password required"},
                status=400
            )

        await create_user(username, password)
        return JsonResponse({"message": "User created successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


@csrf_exempt
async def login_view(request):
    if request.method != "POST":
        return JsonResponse({"message": "Use POST method for login"}, status=405)

    try:
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password required"},
                status=400
            )

        user = await authenticate_user(username, password)
        if user:
            await login_user(request, user)
            return JsonResponse({"message": "Login success"})

        return JsonResponse({"error": "Invalid credentials"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


@csrf_exempt
async def logout_view(request):
    await logout_user(request)
    return JsonResponse({"message": "Logged out successfully"})


# ================= PROFILE APIs =================


@csrf_exempt
def profile_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    if request.method != "GET":
        return JsonResponse({"message": "Use GET method"}, status=405)

    profile, created = Profile.objects.get_or_create(user=request.user)

    return JsonResponse({
        "username": request.user.username,
        "email": request.user.email,
    })


@csrf_exempt
def profile_update(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    if request.method != "POST":
        return JsonResponse({"message": "Use POST method"}, status=405)

    try:
        body = json.loads(request.body)
        phone = body.get("phone", "")
        address = body.get("address", "")

        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.phone = phone
        profile.address = address
        profile.save()

        return JsonResponse({
            "message": "Profile updated successfully",
            "phone": profile.phone,
            "address": profile.address
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    
def signup_form(request):
    return render(request, "signup.html")

def login_form(request):
    return render(request, "login.html")

def profile_form(request):
    return render(request, "profile.html")