import os
import json
import random
import string

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from app.face_capture import main
from app.face_detection import run

# Load users and admin data from JSON
with open(settings.DATA_URL, "r") as f:
    users_data = json.load(f)

with open(settings.ADMIN_URL, "r") as f:
    admin_data = json.load(f)


# -----------------------------
# Views
# -----------------------------

def home(request):
    return render(request, "home.html")


def admin(request):
    return render(request, "admin_login.html")


def user(request):
    return render(request, "user.html")


def show_user(request):
    if request.method == "GET":
        return redirect("/")

    email = request.POST.get("email")
    password = request.POST.get("password")

    if not (user := users_data.get(email)):
        return redirect("/user")
    elif user["password"] == password:
        return render(request, "show_user.html", {"user_data": user, "email": email})
    else:
        return redirect("/user")


def show_users(request):
    if request.method == "GET":
        return redirect("/")

    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username, password)

    if admin_data["adminuser"] == username and admin_data["adminpassword"] == password:
        return render(request, "user_details.html", {"users_data": users_data})
    else:
        return redirect("/admin")


def vote(request):
    voter_id = request.POST.get("voter_id")
    user_data = users_data[voter_id]
    user_data["Voted"] = "Yes"

    with open(settings.DATA_URL, "w") as f:
        json.dump(users_data, f)

    return render(request, "message.html")


def user_login(request):
    return render(request, "user_login.html")


def upload_file(upload):
    fss = FileSystemStorage()
    file = fss.save(upload.name, upload)
    file_url = fss.url(file)
    return file_url


def detect_face(request):
    email = request.POST.get("email")
    user_data = users_data[email]

    profile_image_name = os.path.basename(user_data["Photo"])
    image_url = os.path.join(settings.BASE_DIR, "media", profile_image_name)

    file_name = main()
    captured_img_url = os.path.join(settings.BASE_DIR, "media", file_name)

    try:
        if run(image_one=image_url, image_two=captured_img_url):
            print("same people")
            otp_value = ''.join(random.choices(string.digits, k=4))
            return render(request, "otp.html", {"otp": otp_value})
    finally:
        if os.path.exists(captured_img_url):
            os.remove(captured_img_url)

    return render(request, "user.html")


def add(request):
    request_data = request.POST.copy()
    _ = request_data.pop("csrfmiddlewaretoken")

    file_url = upload_file(request.FILES['image'])
    email = request_data.get("email")

    request_data["Photo"] = file_url
    users_data[email] = request_data

    with open(settings.DATA_URL, "w") as f:
        json.dump(users_data, f)

    return redirect("/user")


def add_user_details(request):
    return render(request, "add_user_details.html")


def show_voter_details(request):
    voter_id = str(request.POST.get("voter_id"))
    print(f"{voter_id=}")

    if not (user_data := users_data.get(voter_id)):
        return redirect("/")
    else:
        return render(request, "show_user.html", {"user_data": user_data, "voter_id": voter_id})
