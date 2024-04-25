from django.urls import path
from . import views

app_name = "chatgpt"
urlpatterns = [
    path("translate/", views.TranslateAPIView.as_view(), name="translate"),
]
