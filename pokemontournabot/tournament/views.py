import math

from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets


from .models import tournament, player, registration, match, player_in_match
from .forms import create_tournament_form, create_player_form, register_player_form
from .serializer import PlayerSerializer, MatchSerializer, TournamentSerializer, RegistrationSerializer, PlayerInMatchSerializer
# Create your views here.

# rest API

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = player.objects.all().order_by('name')
    serializer_class = PlayerSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = match.objects.all().order_by('name')
    serializer_class = MatchSerializer

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = tournament.objects.all().order_by('id')
    serializer_class = TournamentSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = registration.objects.all().order_by('id')
    serializer_class = RegistrationSerializer

class PlayerInMatchViewSet(viewsets.ModelViewSet):
    queryset = player_in_match.objects.all().order_by('id')
    serializer_class = PlayerInMatchSerializer

## login view

def login_page(request):
    """ print home"""
    template = loader.get_template('login_page.html')
    context = {}
    return HttpResponse(template.render(context, request))

def user_login(request):
    """Authenticate a user."""

    if 'username' in request.POST:
        username = request.POST['username']
    else:
        username = ''
    
    if 'password' in request.POST:
        password = request.POST['password']
    else:
        password = ''
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        messages.add_message(request, messages.SUCCESS, "connected")
        return redirect("home")
    else:
        messages.add_message(
            request, messages.ERROR, "wrong login"
        )
        return redirect("login_page")

def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "logged out")
    return redirect("login_page")

def home(request):
    """ print home"""
    if not request.user.is_authenticated:
        return redirect('login_page')
    template = loader.get_template('home.html')
    context = {}
    context['tournaments'] = tournament.objects.order_by('name').all()
    return HttpResponse(template.render(context, request))

def template_create_player(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    context = {}
    template = loader.get_template('create_player.html')
    form = create_player_form()
    context['form'] = form
    return HttpResponse(template.render(context, request))

def create_player(request):
    if request.method == 'POST':
        form = create_player_form(request.POST)
        if form.is_valid():
            create_player = player.objects.get_or_create(
                name=form['name'].value(),
                gamer_id=2,
                elo=1000)
            return redirect('home')
        return redirect('home')
    return redirect('home')


def template_register_player(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    context = {}
    template = loader.get_template('register_player.html')
    form = register_player_form()
    context['form'] = form
    return HttpResponse(template.render(context, request))

def register_player(request):
    if request.method == 'POST':
        form = register_player_form(request.POST)
        if form.is_valid():
            registered_player = registration.objects.get_or_create(
                tournament=tournament.objects.filter(id=form['tournament'].value()).first(), 
                player=player.objects.filter(id=form['player'].value()).first()
                )
            return redirect('home')
        return redirect('home')
    return redirect('home')


def template_create_tournament(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    context = {}
    template = loader.get_template('create_tournament.html')
    form = create_tournament_form()
    context['form'] = form
    return HttpResponse(template.render(context, request))

def create_tournament(request):
    if request.method == 'POST':
        form = create_tournament_form(request.POST)
        if form.is_valid():
            created_tournament = tournament.objects.get_or_create(
                name=form['name'].value(), 
                date=form['date'].value(),
                is_started=False)
            return redirect('home')
        return redirect('home')
    return redirect('home')

def tournament_view(request, tournament_id):
    if not request.user.is_authenticated:
        return redirect('login_page')

    tour = tournament.objects.filter(id=tournament_id).first()
    matchs = match.objects.filter(tournament=tour).order_by('id').all()
    registered_players = player.objects.filter(id__in=[r.player.id for r in registration.objects.filter(tournament=tour)])
    # print(registration.objects.filter(tournament=tour))
    # print(registered_players)
    context = {}
    context['tournament_name'] = tour.name
    context['tournament_id'] = tour.id
    context['matchs'] = matchs
    context['rplayers'] = registered_players
    template = loader.get_template('tournament.html')
    return HttpResponse(template.render(context, request))

@api_view(['POST'])
def make_tournament_tree(request, tournament_id):
    
    tour = tournament.objects.filter(id=tournament_id).first()

    players = player.objects.filter(id__in=[r.player.id for r in registration.objects.filter(tournament_id=tournament_id).all()]).order_by('elo').all()
    # print(players)

    sf_list = []
    qf_list = []
    r16_list = []
    r32_list = []
    r64_list= []

    # create match tree

    print(math.ceil(len(players)/8))
    print(len(players))
    nb_match = math.ceil(len(players)/8)
    if nb_match > 0 :
        f_match = match.objects.get_or_create(
            match_rank='FINAL',
            tournament=tour,
            name=tour.name+' - FINAL',
            finished=False
        )
    if nb_match > 1 :
        for i in range(2):
            sf = match.objects.get_or_create(
                match_rank='SEMI-FINAL',
                tournament=tour,
                name=tour.name+' - SEMI-FINAL #' +str(i),
                next_match_id = f_match[0].id,
                finished=False
            )
            sf_list.append(sf[0])
    if nb_match > 2 :
        for i in range(4):
            qf = match.objects.get_or_create(
                match_rank='QUARTER-FINAL',
                tournament=tour,
                name=tour.name+' - QUARTER-FINAL #' +str(i),
                next_match_id = sf_list[math.floor(i/2)].id,
                finished=False
            )
            qf_list.append(qf[0])
    if nb_match > 4 :
        for i in range(8):
            r16 = match.objects.get_or_create(
                match_rank='ROUND OF 16',
                tournament=tour,
                name=tour.name+' - ROUND OF 16 #' +str(i),
                next_match_id = qf_list[math.floor(i/2)].id,
                finished=False
            )
            r16_list.append(r16)
    if nb_match > 8 :
        for i in range(16):
            r32 = match.objects.get_or_create(
                match_rank='ROUND OF 32',
                tournament=tour,
                name=tour.name+' - ROUND OF 32 #' +str(i),
                next_match_id = qf_list[math.floor(i/2)].id,
                finished=False
            )
            r32_list.append(r32[0])
    if nb_match > 16 :
        for i in range(32):
            r64 = match.objects.get_or_create(
                match_rank='ROUND OF 64',
                tournament=tour,
                name=tour.name+' - ROUND OF 64 #' +str(i),
                next_match_id = qf_list[math.floor(i/2)].id,
                finished=False
            )
            r64_list.append(r64[0])

    # fill match tree
    print(sf_list)
    print(qf_list)
    print(players)
    pos = 0
    if nb_match > 16 :
        for p in players:
            pos += 1
            pm = player_in_match(player=p, match=r64_list[pos%32])
            pm.save()
    elif nb_match > 8 :
        for p in players:
            pos += 1
            pm = player_in_match(player=p, match=r32_list[pos%16])
            pm.save()
    elif nb_match > 4 :
        for p in players:
            pos += 1
            pm = player_in_match(player=p, match=r16_list[pos%8])
            pm.save()
    elif nb_match > 2 :
        for p in players:
            pos += 1
            pm = player_in_match(player=p, match=qf_list[pos%4])
            pm.save()
    elif nb_match > 1 :
        for p in players:
            print(p)
            pos += 1
            pm = player_in_match(player=p, match=sf_list[pos%2])
            pm.save()
    else:
        for p in players:
            pos += 1
            pm = player_in_match(player=p, match=f_match[0])
            pm.save()

    return redirect('tournament', tournament_id=tournament_id)

def match_view(request, match_id):
    if not request.user.is_authenticated:
        return redirect('login_page')

    match_v = match.objects.filter(id=match_id).first()
    players = player.objects.filter(id__in=[r.player.id for r in player_in_match.objects.filter(match=match_v)]).order_by('id').all()
    context = {}
    context['match_name'] = match_v.name
    context['players'] = players
    template = loader.get_template('match.html')
    return HttpResponse(template.render(context, request))
