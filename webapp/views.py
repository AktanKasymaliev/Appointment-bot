from collections import defaultdict
from email.policy import default
from rest_framework import generics, response, views, status
from django.db.models import Q, Count

from webapp.models import Applicant, Card, Queue
from webapp.serializers import CreateApplicantAccountSerializer,\
                                ApplicantSerializer, NewQueueSerializer,\
                                GetFirstFreeCardSerializer

class CreateApplicantAccountView(generics.UpdateAPIView):
    serializer_class = CreateApplicantAccountSerializer
    queryset = Applicant.objects.all()

    def put(self, request, *args, **kwargs):
        return response.Response("Put method is unavailable")

class ApplicantDetailView(generics.RetrieveAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

class GetApplicantsListView(views.APIView):

    def get(self, request):
        applicants = (Applicant.objects
            .filter(is_success=False, is_busy=False)
            .values('visa_centre', 'subcategory')
            .annotate(Count('subcategory'))
        )
        response_data = []
        for data in applicants:
            response_data.append(
                (data['visa_centre'], data['subcategory'], data['subcategory__count'])
            )
        return response.Response(response_data)

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

    def post(self, request):
        from_num = request.POST.get('From')
        to_num = request.POST.get('To')
        text = request.POST.get('Body')
        print(f"From: {from_num}\nTo Number: {to_num}\nText: {text}")
        return response.Response("Sms incomed", status.HTTP_201_CREATED)

class CatchFreeWindowsView(views.APIView):

    def post(self, request):
        visa_centre = request.POST.get('visa_centre')
        subcategory = request.POST.get('subcategory')
        free_windows = request.POST.get('free_windows')
        print(visa_centre, subcategory, free_windows)
        return response.Response({"All right"})