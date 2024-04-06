from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from .dependencies import get_guess_game_service
from .models import Player
from .serializers import (
    AnswerSerializer,
    PlayerCreateSerializer,
    PlayerSerializer,
)
from .services import GuessNumberEstimation, NoSuchPlayer, PlayerAlreadyExists

# Create your views here.


class PlayerCreateAPIView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerCreateSerializer

    def create(self, request: Request) -> Response:
        player = self.serializer_class(data=request.data)

        if not player.is_valid():
            return Response({"error": "Invalid data"}, status=400)

        player_data = player.validated_data

        guess_game_service = get_guess_game_service()

        try:
            guess_game_service.create_new_player(
                player_data["telegram_username"]
            )
        except PlayerAlreadyExists:
            return Response({"error": "Player already exists"}, status=409)

        return Response(status=201)


class PlayerRetrieveAPIView(generics.RetrieveAPIView):
    lookup_field = "telegram_username"

    def retrieve(self, request: Request, telegram_username: str) -> Response:
        guess_game_service = get_guess_game_service()

        try:
            player_progress_dto = guess_game_service.get_progress(
                telegram_username
            )

            return Response(
                {
                    "level": player_progress_dto.level,
                    "expirience_to_level_up_left": (
                        player_progress_dto.expirience_to_level_up_left
                    ),
                },
                status=200,
            )

        except NoSuchPlayer:
            return Response(
                {"error": "No user with such username"}, status=404
            )


class AnswerCreateAPIView(generics.CreateAPIView):
    serializer_class = AnswerSerializer

    def create(self, request: Request) -> Response:
        user_answer = self.serializer_class(data=request.data)

        if not user_answer.is_valid():
            return Response({"error": "Invalid data"}, status=400)

        user_answer_data = user_answer.data

        user_guess = user_answer_data["number"]

        guess_game_service = get_guess_game_service()

        try:
            estimation = guess_game_service.check_answer(
                user_guess, user_answer_data["telegram_username"]
            )

        except NoSuchPlayer:
            return Response({"error": "Player not found"}, status=404)

        if estimation == GuessNumberEstimation.LESS:
            return Response({"estimation": "LESS"})

        if estimation == GuessNumberEstimation.GREATER:
            return Response({"estimation": "GREATER"})

        if estimation == GuessNumberEstimation.RIGHT_ANSWER:
            return Response({"estimation": "RIGHT_ANSWER"})

        raise Exception("This way should've never been reached")
