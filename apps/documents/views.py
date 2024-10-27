from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from apps.documents.models import Types
from apps.documents.serializers import TypesSerializer


class TypesListViewSet(ListAPIView):
    queryset = Types.objects.all()
    serializer_class = TypesSerializer
    permission_classes = [AllowAny]
