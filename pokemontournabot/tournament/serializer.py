from rest_framework import serializers
from .models import tournament, player, registration, match, player_in_match


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model=player
        fields=('name','gamer_id','elo')

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = match
        fields =('name', 'match_rank', 'finished', 'tournament')

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = tournament
        fields =('name', 'date', 'is_started')

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = registration
        fields =('tournament', 'player')

class PlayerInMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = player_in_match
        fields =('match', 'result_pos', 'player')