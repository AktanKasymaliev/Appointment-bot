from rest_framework import generics, response, views, status

from webapp.models import Applicant, Card, Queue
from webapp.serializers import CreateApplicantAccountSerializer,\
     ApplicantDetailSerializer, NewQueueSerializer, GetFirstFreeCardSerializer

class CreateApplicantAccountView(generics.RetrieveUpdateAPIView):
    serializer_class = CreateApplicantAccountSerializer
    queryset = Applicant.objects.all()

    def put(self, request, *args, **kwargs):
        return response.Response("Put method is unavailable")

class ApplicantDetailView(generics.RetrieveAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantDetailSerializer

class GetFirstFreeCardView(views.APIView):

    def __return_response(self, data, status):
        return response.Response(data, status=status)

    def get(self, request):
        free_card = Card.objects.filter(is_busy=False).first()
        
        if free_card is not None: 
            return self.__return_response(
                GetFirstFreeCardSerializer(free_card).data, 
                status=status.HTTP_200_OK)

        return self.__return_response({
            "Card": "No content"
        }, status=status.HTTP_204_NO_CONTENT)


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
        
class GetSmsCodeView(views.APIView):

    def get(self, request):
        print(request)

    def post(self, request):
        from_num = request.POST.get('From',)
        to_num = request.POST.get('To')
        text = request.POST.get('Body')
        print(f"From: {from_num}\nTo Number: {to_num}\nText: {text}")