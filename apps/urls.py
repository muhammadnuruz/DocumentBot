from django.urls import path, include

urlpatterns = [
    path('analyses/', include("apps.analyses.urls")),
    path('telegram-users/', include("apps.telegram_users.urls")),
    path('documents/', include("apps.documents.urls")),
]
