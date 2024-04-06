from django.urls import path

from .views import (
    AnswerCreateAPIView,
    PlayerCreateAPIView,
    PlayerRetrieveAPIView,
)

guess_number_game_urlpatterns = [
    path("api/v1/players", PlayerCreateAPIView.as_view()),
    path(
        "api/v1/players/<str:telegram_username>",
        PlayerRetrieveAPIView.as_view(),
    ),
    path("api/v1/answer", AnswerCreateAPIView.as_view()),
]
