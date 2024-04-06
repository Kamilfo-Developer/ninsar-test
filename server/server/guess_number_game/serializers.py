from rest_framework import serializers

from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class PlayerProgressSerializer(serializers.Serializer):
    level = serializers.IntegerField()
    expirience_to_level_up_left = serializers.IntegerField()


class PlayerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["telegram_username"]


class AnswerSerializer(serializers.Serializer):
    telegram_username = serializers.CharField()
    number = serializers.IntegerField()

    def validate_number(self, number):
        is_valid = number in set(range(1, 101))

        if not is_valid:
            raise serializers.ValidationError(
                "Value of number should be in range 1-100 inclusive"
            )

        return number
