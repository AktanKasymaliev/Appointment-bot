from rest_framework import generics, response

from webapp.models import Applicant
from webapp.serializers import CreateApplicantAccountSerializer

class CreateApplicantAccountView(generics.RetrieveUpdateAPIView):
    serializer_class = CreateApplicantAccountSerializer
    queryset = Applicant.objects.all()

    def put(self, request, *args, **kwargs):
        return response.Response("Put method is unavailable")