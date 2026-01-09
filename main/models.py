from django.db import models

class Users(models.Model):
    steamid = models.CharField(max_length=20, primary_key=True)
    personaname = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255)
    friends = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        through='Friendship',
        through_fields=('from_user', 'to_user'),
    )
    friends_last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.personaname} ({self.steamid})"


class Friendship(models.Model):
    from_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='friendship_creator_set')
    to_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='friend_of_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} friends with {self.to_user}"


class Game(models.Model):
    appid = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    icon_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class UserGameStats(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='game_stats')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='user_stats')
    playtime_forever = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.personaname} - {self.game.name}: {self.playtime_forever} min"
