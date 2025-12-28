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
    genre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Achievement(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='achievements')
    apiname = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon_url = models.URLField()
    hidden = models.BooleanField(default=False)

    class Meta:
        unique_together = ('game', 'apiname')

    def __str__(self):
        return f"{self.game.name} - {self.display_name}"


class UserGameStats(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='game_stats')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='user_stats')
    playtime_forever = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.personaname} - {self.game.name}: {self.playtime_forever} min"


class UserAchievement(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='unlocked_by')
    unlock_time = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.personaname} unlocked '{self.achievement.display_name}'"