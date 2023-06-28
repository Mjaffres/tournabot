from django.urls import path, re_path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'match', views.MatchViewSet, basename='match')
router.register(r'player', views.PlayerViewSet, basename='player')
router.register(r'tournament', views.TournamentViewSet, basename='tournament')
router.register(r'registration', views.RegistrationViewSet, basename='registration')

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.home, name='home'),
    path('login_page', views.login_page, name='login_page'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('tournament/template_create', views.template_create_tournament, name='template_create_tournament'),
    path('tournament/create', views.create_tournament, name = 'create_tournament'),
    path('tournament/<int:tournament_id>', views.tournament_view, name = 'tournament'),
    path('tournament/<int:tournament_id>/make_tree', views.make_tournament_tree, name = 'make_tournament_tree'),
    path('match/<int:match_id>', views.match_view, name = 'match'),
    path('player/template_create', views.template_create_player, name = 'template_create_player'),
    path('player/create', views.create_player, name = 'create_player'),
    path('player/template_register', views.template_register_player, name = 'template_register_player'),
    path('player/register', views.register_player, name = 'register_player'),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework'))
] + router.get_urls()