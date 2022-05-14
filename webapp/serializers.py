from rest_framework import serializers

from webapp.models import Applicant

class CreateApplicantAccountSerializer(serializers.ModelSerializer):
    BULK_UPDATE_FIELDS = ('email', 'email_password', 'settlement', 'vfs_account')
    
    class Meta:
        model = Applicant
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')
        instance.email_password = validated_data.get('email_password')
        instance.settlement = validated_data.get('settlement')
        instance.vfs_account = validated_data.get('vfs_account')

        Applicant.objects.bulk_update(
            [instance],
            fields=self.BULK_UPDATE_FIELDS)

        return instance