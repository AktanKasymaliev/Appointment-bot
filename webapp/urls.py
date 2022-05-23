from django.urls import path

from webapp.views import ApplicantDetailView, CatchFreeWindowsView, CheckSmsCodeView,\
                     CreateApplicantAccountView, GetApplicantsListView, GetFirstFreeCardView, GetSmsCodeView,\
                     NewQueueView

urlpatterns = [
    path('create-applicant-account/<int:pk>/', CreateApplicantAccountView.as_view()),
    path('get-applicant-data/<int:pk>/', ApplicantDetailView.as_view()),
    path('get-applicants-data/', GetApplicantsListView.as_view()),

    path('get-first-free-card/', GetFirstFreeCardView.as_view()),

    path('create-new-sms-queue/', NewQueueView.as_view()),
    path('check-sms-code/<int:applicant_id>/<int:card_id>/', CheckSmsCodeView.as_view()),
    path('twilio-sms-code-webhook/', GetSmsCodeView.as_view()),

    path('catch-free-windows/', CatchFreeWindowsView.as_view())
]
