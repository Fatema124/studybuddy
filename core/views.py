from datetime import datetime

from bson import ObjectId
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from .mongo_connection import (
    groups_col,
    join_form_requests_col,
    group_suggestions_col,
    help_requests_col,
    group_feedback_col,
    tutor_applications_col,
)


# ===================== PUBLIC PAGES =====================

def home(request):
    """
    Home page – list study groups with optional search.
    """
    search = request.GET.get("search", "").strip()

    query = {}
    if search:
        query = {"title": {"$regex": search, "$options": "i"}}

    groups = list(groups_col.find(query))

    context = {
        "groups": groups,
        "search": search,
    }
    return render(request, "core/home.html", context)


# ---------- Function 1 – Join a study group ----------

def join_group(request):
    """
    Function 1 – Join a study group (saves a join request in MongoDB).
    """
    if request.method == "POST":
        full_name = request.POST.get("full_name", "")
        email = request.POST.get("email", "")
        course_code = request.POST.get("course_code", "")
        message = request.POST.get("message", "")

        doc = {
            "full_name": full_name,
            "email": email,
            "course_code": course_code,
            "message": message,
            "requested_at": datetime.utcnow(),
        }
        join_form_requests_col.insert_one(doc)
        return redirect("join_success")

    return render(request, "core/join_group.html")


def join_success(request):
    return render(request, "core/join_success.html")


def view_requests(request):
    """
    Helper page – list all join requests from MongoDB.
    """
    requests_list = list(
        join_form_requests_col.find().sort("requested_at", -1)
    )

    context = {
        "requests": requests_list,
    }
    return render(request, "core/requests.html", context)


# ---------- Function 2 – Suggest a new study group ----------

def suggest_group(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "")
        email = request.POST.get("email", "")
        course_code = request.POST.get("course_code", "")
        suggested_title = request.POST.get("suggested_title", "")
        preferred_mode = request.POST.get("preferred_mode", "")
        notes = request.POST.get("notes", "")

        doc = {
            "full_name": full_name,
            "email": email,
            "course_code": course_code,
            "suggested_title": suggested_title,
            "preferred_mode": preferred_mode,
            "notes": notes,
            "submitted_at": datetime.utcnow(),
        }
        group_suggestions_col.insert_one(doc)
        return redirect("suggest_group_success")

    return render(request, "core/suggest_group.html")


def suggest_group_success(request):
    return render(request, "core/suggest_group_success.html")


# ---------- Function 3 – Request one-to-one help session ----------

def help_request(request):
    if request.method == "POST":
        student_name = request.POST.get("student_name", "")
        email = request.POST.get("email", "")
        course_code = request.POST.get("course_code", "")
        topic = request.POST.get("topic", "")
        preferred_time = request.POST.get("preferred_time", "")

        doc = {
            "student_name": student_name,
            "email": email,
            "course_code": course_code,
            "topic": topic,
            "preferred_time": preferred_time,
            "status": "pending",
            "created_at": datetime.utcnow(),
        }
        help_requests_col.insert_one(doc)
        return redirect("help_request_success")

    return render(request, "core/help_request.html")


def help_request_success(request):
    return render(request, "core/help_request_success.html")


# ---------- Function 4 – Leave feedback on a study group ----------

def feedback(request):
    if request.method == "POST":
        group_title = request.POST.get("group_title", "")
        student_name = request.POST.get("student_name", "")
        rating_str = request.POST.get("rating", "0")
        comment = request.POST.get("comment", "")

        try:
            rating = int(rating_str)
        except ValueError:
            rating = 0

        doc = {
            "group_title": group_title,
            "student_name": student_name,
            "rating": rating,
            "comment": comment,
            "created_at": datetime.utcnow(),
        }
        group_feedback_col.insert_one(doc)
        return redirect("feedback_success")

    return render(request, "core/feedback.html")


def feedback_success(request):
    return render(request, "core/feedback_success.html")


# ---------- Function 5 – Tutor signup (volunteer mentor) ----------

def tutor_signup(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "")
        email = request.POST.get("email", "")
        major = request.POST.get("major", "")
        year_level_str = request.POST.get("year_level", "")
        courses_can_help = request.POST.get("courses_can_help", "")

        try:
            year_level = int(year_level_str)
        except ValueError:
            year_level = None

        doc = {
            "full_name": full_name,
            "email": email,
            "major": major,
            "year_level": year_level,
            "courses_can_help": courses_can_help,
            "approved": False,
            "created_at": datetime.utcnow(),
        }
        tutor_applications_col.insert_one(doc)
        return redirect("tutor_signup_success")

    return render(request, "core/tutor_signup.html")


def tutor_signup_success(request):
    return render(request, "core/tutor_signup_success.html")


# ===================== OWNER / ADMIN PAGES =====================

@staff_member_required
def manage_tutor_applications(request):
    """
    Owner view – list all tutor applications and show approve button.
    """
    applications = []
    cursor = tutor_applications_col.find().sort("created_at", -1)

    for doc in cursor:
        # safe id for template (no leading underscore)
        doc["mongo_id"] = str(doc["_id"])
        applications.append(doc)

    context = {
        "applications": applications,
    }
    return render(request, "core/manage_tutor_applications.html", context)


@staff_member_required
def approve_tutor_application(request, application_id):
    """
    Set approved = True for a specific tutor application.
    """
    if request.method == "POST":
        try:
            oid = ObjectId(application_id)
        except Exception:
            return redirect("manage_tutor_applications")

        tutor_applications_col.update_one(
            {"_id": oid},
            {"$set": {"approved": True}}
        )

    return redirect("manage_tutor_applications")


@staff_member_required
def manage_feedback(request):
    """
    Owner view – list feedback with simple text filter.
    """
    q = request.GET.get("q", "").strip()

    query = {}
    if q:
        query = {
            "$or": [
                {"group_title": {"$regex": q, "$options": "i"}},
                {"comment": {"$regex": q, "$options": "i"}},
            ]
        }

    feedback_list = list(
        group_feedback_col.find(query).sort("created_at", -1)
    )

    context = {
        "feedback_list": feedback_list,
        "q": q,
    }
    return render(request, "core/manage_feedback.html", context)
