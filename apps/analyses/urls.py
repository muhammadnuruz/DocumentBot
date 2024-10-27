from django.urls import path

from apps.analyses.views import DocumentsDetailViewSet, DocumentsCreateViewSet, DocumentsChatIdDetailViewSet

urlpatterns = [
    path('create/', DocumentsCreateViewSet.as_view(),
         name='documents-create'),
    path('chat_id/<str:chat_id>/', DocumentsChatIdDetailViewSet.as_view(),
         name='documents-chat_id'),
    path('detail/<int:pk>/', DocumentsDetailViewSet.as_view(),
         name='documents-detail')
]
