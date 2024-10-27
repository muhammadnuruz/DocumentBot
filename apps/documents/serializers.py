from apps.documents.models import Types
from rest_framework import serializers


class TypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Types
        fields = '__all__'