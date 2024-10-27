from django.urls import path

from apps.documents.views import TypesListViewSet

urlpatterns = [
    path('', TypesListViewSet.as_view(),
         name='types-list'),
]
