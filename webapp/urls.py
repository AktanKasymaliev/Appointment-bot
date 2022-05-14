from django.urls import path

from webapp.views import CreateApplicantAccountView

urlpatterns = [
    path('create/applicant/account/<int:pk>/', CreateApplicantAccountView.as_view())
]
