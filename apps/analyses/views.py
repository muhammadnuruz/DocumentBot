from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from apps.analyses.models import Documents
from apps.analyses.serializers import DocumentsSerializer, DocumentsCreateSerializer


class DocumentsDetailViewSet(RetrieveAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer
    permission_classes = [AllowAny]


class DocumentsChatIdDetailViewSet(RetrieveAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        chat_id = self.kwargs.get('chat_id')
        return get_object_or_404(Documents, chat_id=chat_id)


class DocumentsCreateViewSet(CreateAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentsCreateSerializer
    permission_classes = [AllowAny]
