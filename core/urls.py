from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Join study group
    path("join/", views.join_group, name="join_group"),
    path("join/success/", views.join_success, name="join_success"),

    # View join requests
    path("requests/", views.view_requests, name="view_requests"),

    # Function 2 – Suggest a new study group
    path("suggest-group/", views.suggest_group, name="suggest_group"),
    path("suggest-group/success/", views.suggest_group_success, name="suggest_group_success"),

    # Function 3 – Request one-to-one help session
    path("help-request/", views.help_request, name="help_request"),
    path("help-request/success/", views.help_request_success, name="help_request_success"),

    # Function 4 – Leave feedback on a study group
    path("feedback/", views.feedback, name="feedback"),
    path("feedback/success/", views.feedback_success, name="feedback_success"),

    # Function 5 – Register as a volunteer tutor / mentor
    path("tutor-signup/", views.tutor_signup, name="tutor_signup"),
    path("tutor-signup/success/", views.tutor_signup_success, name="tutor_signup_success"),

    # Owner/admin pages for Mongo data
    path(
        "owner/tutor-applications/",
        views.manage_tutor_applications,
        name="manage_tutor_applications",
    ),
    path(
        "owner/tutor-applications/<str:application_id>/approve/",
        views.approve_tutor_application,
        name="approve_tutor_application",
    ),
    path(
        "owner/feedback/",
        views.manage_feedback,
        name="manage_feedback",
    ),
]
