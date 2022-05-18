from rest_framework import generics, response

from webapp.models import Applicant
from webapp.serializers import CreateApplicantAccountSerializer, ApplicantDetailSerializer

class CreateApplicantAccountView(generics.RetrieveUpdateAPIView):
    serializer_class = CreateApplicantAccountSerializer
    queryset = Applicant.objects.all()

    def put(self, request, *args, **kwargs):
        return response.Response("Put method is unavailable")

class ApplicantDetailView(generics.RetrieveAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantDetailSerializer

class WaitSmsApplicantPaymentView():
    pass