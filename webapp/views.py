from rest_framework import generics, response, views

from webapp.models import Applicant, Queue
from webapp.serializers import CreateApplicantAccountSerializer,\
     ApplicantDetailSerializer, NewQueueSerializer

class CreateApplicantAccountView(generics.RetrieveUpdateAPIView):
    serializer_class = CreateApplicantAccountSerializer
    queryset = Applicant.objects.all()

    def put(self, request, *args, **kwargs):
        return response.Response("Put method is unavailable")

class ApplicantDetailView(generics.RetrieveAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantDetailSerializer

class NewQueueView(generics.CreateAPIView):
    # POST endpoint for creating queue with applicant_id, card_id
    serializer_class = NewQueueSerializer

class CheckSmsCodeView(views.APIView):
    # GET endpoint for checking sms_code

    def get(self, request, applicant_id):
        queue_instance = Queue.objects.get(applicant_id=applicant_id)
        code = queue_instance.sms_code

        if code is not None:
            return response.Response({"sms_code": code})

        return response.Response({
            "sms_code": None
        })