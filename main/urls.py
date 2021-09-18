from django.urls import path

from main.views import upload_voter, fill_voter, generate_pdf, voters_list, delete_voter

urlpatterns = [
    path("upload-voter/", upload_voter, name="upload-voter"),
    path('voters-list', voters_list, name='voters-list'),
    path("fill-voter/<int:id>", fill_voter, name="fill-voter"),
    path("delete-voter/<int:id>", delete_voter, name="delete-voter"),
    path("pdf/<int:id>", generate_pdf, name="pdf"),
]
