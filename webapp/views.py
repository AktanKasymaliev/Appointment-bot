from rest_framework import generics, response, views, status

from webapp.models import Applicant, Card, Queue
from webapp.serializers import CreateApplicantAccountSerializer,\
     ApplicantDetailSerializer, GetCardListSerializer, NewQueueSerializer

class CreateApplicantAccountView(generics.RetrieveUpdateAPIView):
    serializer_class = CreateApplicantAccountSerializer
    queryset = Applicant.objects.all()

    def put(self, request, *args, **kwargs):
        return response.Response("Put method is unavailable")

class ApplicantDetailView(generics.RetrieveAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantDetailSerializer

class GetCardListView(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = GetCardListSerializer

class NewQueueView(generics.CreateAPIView):
    # POST endpoint for creating queue with applicant_id, card_id
    serializer_class = NewQueueSerializer

class CheckSmsCodeView(views.APIView):
    # GET endpoint for checking sms_code

    def __return_no_content(self):
        return response.Response({
                "sms_code": "No content"
            }, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, applicant_id, card_id):
        try:
            code = Queue.objects.get(
                applicant_id=applicant_id, card_id=card_id
                ).sms_code

            if code is not None:
                return response.Response({"sms_code": code}, status=status.HTTP_200_OK)
            else:
                self.__return_no_content()
                
        except Queue.DoesNotExist:
            self.__return_no_content()