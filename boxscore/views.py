from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Boxscore, Team, Game
from .forms import BoxscoreForm
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your views here.
"""
def login(request):
    if request.method == "POST":
        return render(request, 'boxscore/statics.html')
    else:
        return render(request, 'boxscore/login.html')
"""
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        email = request.POST.get('email')
        if not username or not raw_password or not email:
            return render(request, 'boxscore/register.html', {'error': "please fill in all of the blanks."})

        elif User.objects.filter(username=username) or User.objects.filter(email=email):
            return render(request, 'boxscore/register.html', {'error': "username or email used."})

        else:
            user = User.objects.create_user(username, email, raw_password)
            return render(request, 'boxscore/statics.html', {'succeed': "Registered!"})

    else:
        return render(request, 'boxscore/register.html')

def stat(request):
    game_list = Game.objects.filter(user_under_game=request.user)
    user_teams = Team.objects.filter(team_cap=request.user)
    my_statics = Boxscore.objects.filter(user=request.user).order_by('opponent')
    return render(request, 'boxscore/statics.html', {'my_statics': my_statics})

@login_required
def team_boxscore(request, team_name):
    statics = Boxscore.objects.filter(user=request.user, team_name=team_name).order_by('opponent')
    if not statics:
        statics = Team.objects.filter(team_cap=request.user).order_by('team_name_under_Team')
        return render(request, 'boxscore/add_game.html', {'statics': statics, 'succeed': "Successfully signed up a team. Now updates games for it."})
    team_name = statics.values()[0]['team_name']
    return render(request, 'boxscore/team_boxscore.html', {'statics': statics, 'team_name': team_name})

@login_required
def match_boxscore(request, team_name, opponent):
    statics = Boxscore.objects.filter(user=request.user, team_name=team_name, opponent=opponent).order_by('player')
    return render(request, 'boxscore/match_boxscore.html', {'statics': statics, 'team_name': team_name, 'opponent': opponent})

@login_required
def add_stat(request):
    if request.method == "POST":
        user = request.user
        game_id = request.POST.get('game_name')
        player = request.POST.get('player')
        if not game_id or not player:
            team_options = Team.objects.filter(team_cap=user)
            game_list = Game.objects.filter(user_under_game=request.user)
            return render(request, 'boxscore/add_stat.html', {'error': "Please select a game and input player number.", 'team_options': team_options, 'game_list': game_list})
        game_info = Game.objects.filter(id=game_id).values()
        team_name = game_info[0]['us']
        opponent = game_info[0]['opponent']
        if Boxscore.objects.filter(user=user, team_name=team_name, opponent=opponent, player=player):
            team_options = Team.objects.filter(team_cap=user)
            game_list = Game.objects.filter(user_under_game=request.user)
            return render(request, 'boxscore/add_stat.html', {'error': f"Stat of player #{player} at this match was added.", 'team_options': team_options, 'game_list': game_list})
        fgm = request.POST.get('fgm')
        fga = request.POST.get('fga')
        threepm = request.POST.get('threepm')
        threepa = request.POST.get('threepa')
        ftm = request.POST.get('ftm')
        fta = request.POST.get('fta')
        oreb = request.POST.get('oreb')
        dreb = request.POST.get('dreb')
        ast = request.POST.get('ast')
        stl = request.POST.get('stl')
        blk = request.POST.get('blk')
        tov = request.POST.get('tov')
        pf = request.POST.get('pf')
        form = BoxscoreForm(request.POST)
        Boxscore.objects.create(user=user, team_name=team_name, opponent=opponent, player=player, fgm=fgm, fga=fga, threepm=threepm, threepa=threepa, ftm=ftm, fta=fta, oreb=oreb, dreb=dreb, ast=ast, stl=stl, blk=blk, tov=tov, pf=pf)
        return redirect('team_boxscore', team_name=team_name)
    else:
        team_options = Team.objects.filter(team_cap=request.user)
        game_list = Game.objects.filter(user_under_game=request.user)
        return render(request, 'boxscore/add_stat.html', {'team_options': team_options, 'game_list': game_list})

@login_required
def search(request):
    if request.method == "POST":
        search_by_team_name = request.POST.get('search_by_team_name')
        search_by_player = request.POST.get('search_by_player')
        if not search_by_team_name and not search_by_player:
            statics = Team.objects.filter(team_cap=request.user).order_by('team_name_under_Team')
            matches = Game.objects.filter(user_under_game=request.user).order_by('opponent')
            return render(request, 'boxscore/search.html', {'statics': statics, 'matches':matches, 'error': "Please at least select a match or a team name or input a player number."})
        else:
            if not search_by_player:
                statics = Boxscore.objects.filter(user=request.user, team_name=search_by_team_name).order_by('opponent')
            elif not search_by_team_name:
                statics = Boxscore.objects.filter(user=request.user, player=search_by_player).order_by('player')
            else:
                statics = Boxscore.objects.filter(user=request.user, team_name=search_by_team_name, player=search_by_player).order_by('player')
            return render(request, 'boxscore/result.html', {'statics': statics})
    else:
        statics = Team.objects.filter(team_cap=request.user).order_by('team_name_under_Team')
        matches = Game.objects.filter(user_under_game=request.user).order_by('opponent')
        return render(request, 'boxscore/search.html', {'statics': statics, 'matches': matches})

@login_required
def team_signup(request):
    if request.method == "POST":
        team_name_under_Team = request.POST.get('team_name')
        if not team_name_under_Team:
            return render(request, 'boxscore/team_signup.html', {'error': "Please enter team name."})
        elif Team.objects.filter(team_cap=request.user, team_name_under_Team=team_name_under_Team):
            return render(request, 'boxscore/team_signup.html', {'error': f"This name \'{team_name_under_Team}\' was already signed up by you."})
        else:
            Team.objects.create(team_cap=request.user, team_name_under_Team=team_name_under_Team)
            return redirect('team_boxscore', team_name=team_name_under_Team)# render(request, 'boxscore/team_signup.html')
    else:
        return render(request, 'boxscore/team_signup.html')

@login_required
def games(request):
    games = Game.objects.filter(user_under_game=request.user)
    return render(request, 'boxscore/games.html', {'games': games})

@login_required
def add_game(request):
    if request.method == "POST":
        us = request.POST.get('us')
        opponent = request.POST.get('opponent')
        statics = Team.objects.filter(team_cap=request.user).order_by('team_name_under_Team')
        if not us or not opponent:
            return render(request, 'boxscore/add_game.html', {'statics': statics, 'error': "Please select your team name and fill in the blank."})
        elif Game.objects.filter(user_under_game=request.user, us=us, opponent=opponent):
            return render(request, 'boxscore/add_game.html', {'statics': statics, 'error': "You already updated this match."})
        else:
            Game.objects.create(user_under_game=request.user, us=us, opponent=opponent)
            games = Game.objects.filter(user_under_game=request.user)
            return render(request, 'boxscore/games.html', {'games': games})
    else:
        statics = Team.objects.filter(team_cap=request.user).order_by('team_name_under_Team')
        return render(request, 'boxscore/add_game.html', {'statics': statics})
