# coding=utf-8

from flask import render_template, redirect, request
from app import app
from data.databaseApi import DatabaseAPI


@app.route('/')
@app.route('/index')
def index():
    DatabaseAPI.init_db()
    players = DatabaseAPI.get_players_name()
    # Render template with player data
    return render_template('index.html', players=players)


@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        player_name = request.form.get('playerName')
        print("Add_player_routes:", player_name)
        DatabaseAPI.add_player(player_name)
        return redirect('/')

    # Render the add_player.html template for GET requests
    return render_template('addplayer.html')


@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        selected_players = request.form.getlist('selectedPlayers')
        print("form player: ", selected_players)
        scores = request.form.getlist('playerScore')
        print("form score: ", scores)
        scores = [item for item in scores if item != '']
        print("form score after filter: ", scores)
        holes_played = request.form.get('dataInput')
        print("form hole: ", holes_played)
        DatabaseAPI.add_data(selected_players, scores, holes_played)
        DatabaseAPI.update_player_score(selected_players, scores, holes_played)
        return redirect('/overview')

    # Render the add_player.html template for GET requests
    players = DatabaseAPI.get_players_name()
    # Get only the name
    return render_template('adddata.html', players=players)


@app.route('/overview', methods=['GET'])
def leaderboard():
    playersscore = DatabaseAPI.get_player_score()
    playersname = DatabaseAPI.get_players_name()
    playersname = [player[1] for player in playersname]
    players = DatabaseAPI.get_players_name()
    player_matches = DatabaseAPI.get_player_matches()

    return render_template('leaderboard.html',
                           players=players, playersname=playersname,
                           playersscore=playersscore, player_matches=player_matches)


@app.route('/player/<int:player_id>')
def player_detail(player_id):
    players = DatabaseAPI.get_players_name()
    player_info = DatabaseAPI.get_player_info(player_id)  # Update this method based on your API
    player_matches = DatabaseAPI.get_specific_player_matches(player_id)
    return render_template('player_detail.html',
                           players=players, player_info=player_info, player_matches=player_matches)

