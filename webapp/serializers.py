from rest_framework import serializers

from webapp.models import Applicant, Card, Queue

class CreateApplicantAccountSerializer(serializers.ModelSerializer):
    BULK_UPDATE_FIELDS = ('email', 'email_password', 'vfs_account')
    
    class Meta:
        model = Applicant
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')
        instance.email_password = validated_data.get('email_password')
        instance.vfs_account = validated_data.get('vfs_account')

        Applicant.objects.bulk_update(
            [instance],
            fields=self.BULK_UPDATE_FIELDS)

        return instance

class ApplicantDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicant
        fields = '__all__'

class NewQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Queue
        fields = ('applicant_id', 'card_id')

    def create(self, validated_data):
        return Queue.objects.create(
            **validated_data
        )

class GetFirstFreeCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'