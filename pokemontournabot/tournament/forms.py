from django import forms

from .models import tournament, player, registration, match, player_in_match

class register_player_form(forms.ModelForm):
    class Meta:
        model = registration
        fields = ['player', 'tournament']

class create_player_form(forms.ModelForm):
    class Meta:
        model = player
        fields = ['name']

class create_tournament_form(forms.ModelForm):
    class Meta:
        model = tournament
        fields = ['name', 'date']