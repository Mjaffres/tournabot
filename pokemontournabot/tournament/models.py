from django.db import models

# Create your models here.

class tournament(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateField()
    is_started = models.BooleanField()

    def __str__(self):
        return self.name

class player(models.Model):
    name = models.CharField(max_length=128)
    gamer_id = models.CharField(max_length=128)
    elo = models.BigIntegerField()

    def __str__(self):
        return self.name

class registration(models.Model):
    tournament = models.ForeignKey(tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(player, on_delete=models.CASCADE)

class match(models.Model):
    MATCH_RANK_CHOICES = [
        ("FINAL", "FINAL"),
        ("SEMI-FINAL", "SEMI-FINAL"),
        ("QUARTER-FINAL", "QUARTER-FINAL"),
        ("ROUND OF 64", "ROUND OF 64"),
        ("ROUND OF 128", "ROUND OF 128"),
        ("ROUND OF 256", "ROUND OF 256")
    ]
    name = models.CharField(max_length=128)
    next_match_id = models.BigIntegerField(default=None, blank=True, null=True)
    match_rank = models.CharField(max_length=24,
        choices=MATCH_RANK_CHOICES)
    finished = models.BooleanField()
    tournament = models.ForeignKey(tournament, on_delete=models.CASCADE)

class player_in_match(models.Model):
    match = models.ForeignKey(match, on_delete=models.CASCADE)
    player = models.ForeignKey(player, on_delete=models.CASCADE)
    result_pos = models.BigIntegerField(default=None, blank=True, null=True)