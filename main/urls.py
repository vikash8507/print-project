from django.urls import path

from main.views import home, contact, dashboard, success, upload_voter, fill_voter, generate_pdf, voters_list, delete_voter, pan_list, pan_pdf, new_pan

urlpatterns = [
    path("", home, name="home"),
    path("contact/", contact, name="contact"),
    path("dashboard/", dashboard, name="dashboard"),
    path("success/", success, name="success"),
    path("upload-voter/", upload_voter, name="upload-voter"),
    path('voters-list', voters_list, name='voters-list'),
    path("fill-voter/<int:id>", fill_voter, name="fill-voter"),
    path("delete-voter/<int:id>", delete_voter, name="delete-voter"),
    path("pdf/<int:id>", generate_pdf, name="pdf"),

    path("pan-list/", pan_list, name="pan-list"),
    path("new-pan/", new_pan, name="new-pan"),
    path("pan-pdf/<int:pk>", pan_pdf, name="pan-pdf"),
]
