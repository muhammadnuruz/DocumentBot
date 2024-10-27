from rest_framework import serializers
from .models import Documents


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class DocumentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        exclude = ['created_at', 'updated_at']