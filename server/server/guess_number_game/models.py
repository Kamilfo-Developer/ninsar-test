from __future__ import annotations

from django.db import models

from .dtos import PlayerDTO


# Create your models here.
class Player(models.Model):
    telegram_username = models.CharField(max_length=255)
    level = models.IntegerField(default=0)
    expirience = models.IntegerField(default=0)
    right_answer = models.IntegerField()

    def as_dto(self) -> PlayerDTO:
        return PlayerDTO(
            self.telegram_username,
            self.right_answer,
            self.expirience,
            self.level,
        )

    @staticmethod
    def from_dto(player: PlayerDTO) -> Player:
        return Player(
            telegram_username=player.telegram_username,
            right_answer=player.right_answer,
            level=player.level,
            expirience=player.expirience,
        )
