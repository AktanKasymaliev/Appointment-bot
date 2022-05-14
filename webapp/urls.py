from django.urls import path

from webapp.views import ApplicantDetailView, CreateApplicantAccountView

urlpatterns = [
    path('create-applicant-account/<int:pk>/', CreateApplicantAccountView.as_view()),
    path('get-applicant-data/<int:pk>/', ApplicantDetailView.as_view())
]
