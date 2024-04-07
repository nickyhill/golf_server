import sqlite3


class DatabaseAPI:
    DATABASE = "file:GolfServer.db"
    SCHEMA_FILE = '/var/www/apache-flask/data/GolfServer.sql'

    @staticmethod
    def init_db():
        connection = sqlite3.connect(DatabaseAPI.DATABASE, uri=True)
        with open('/var/www/apache-flask/data/GolfServer.sql') as f:
            connection.executescript(f.read())

        connection.commit()
        connection.close()

    @staticmethod
    def get_players_name():
        with sqlite3.connect(DatabaseAPI.DATABASE, uri=True) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM players')
            players = cursor.fetchall()
            print("Get_player_name;", players)
            return players

    @staticmethod
    def add_player(first_name):
        with sqlite3.connect(DatabaseAPI.DATABASE, uri=True) as conn:
            cursor = conn.cursor()
            print("Add_player: ", first_name)
            print(sqlite3.threadsafety)
            cursor.execute('INSERT INTO players (FirstName) VALUES (?)', (first_name,))
            conn.commit()

    @staticmethod
    def update_player_score(selected_players, scores, holes):
        with (sqlite3.connect(DatabaseAPI.DATABASE, uri=True) as conn):
            cursor = conn.cursor()
            print("update_player_score: ", selected_players, scores)
            # Loop through each selected player and their score
            for player_id, score in zip(selected_players, scores):
                # Fetch the current OverScore for the player
                cursor.execute('SELECT OverScore, HolesPlay FROM Players WHERE PlayerID = ?',
                               (player_id,))
                current_score, current_hole = cursor.fetchone()
                print("DATA player: ", current_score, current_hole)

                # Calculate the new OverScore
                if score.lstrip('-').isdigit():
                    new_score = current_score + int(score)
                new_holes = current_hole + int(holes)
                # Update the OverScore in the Players table
                cursor.execute('UPDATE Players SET OverScore = ?, HolesPlay = ? WHERE PlayerID = ?',
                               (new_score, new_holes, player_id))

            conn.commit()

    @staticmethod
    def get_wins(player_id):
        with sqlite3.connect(DatabaseAPI.DATABASE, uri=True) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT Wins FROM Players WHERE PlayerID = ? ',
                           (player_id, ))
            wins = cursor.fetchone()
            print(wins)
            return wins

    @staticmethod
    def add_data(selected_players, scores, holes_played):
        # Get the form data
        print("add_data: ", selected_players, scores, holes_played)
        # Calculate the lowest score and the winner ID
        int_score = [eval(i) for i in scores]
        lowest_score = min(int_score)
        winner_id = selected_players[scores.index(str(lowest_score))]
        print(winner_id, lowest_score, scores)
        wins_count = DatabaseAPI.get_wins(winner_id)[0]
        print("WINS: ", wins_count)
        wins_count += 1
        # Update new win count into Players
        with sqlite3.connect(DatabaseAPI.DATABASE, uri=True) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Players SET Wins = ? WHERE PlayerID = ?', (wins_count, winner_id))

        # Insert the match into Matches table
        with sqlite3.connect(DatabaseAPI.DATABASE, uri=True) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Matches (MatchDate, WinnerID) VALUES (CURRENT_DATE, ?)', (winner_id,))
            match_id = cursor.lastrowid

            # Insert the match details into MatchDetails table
            for player_id, score in zip(selected_players, scores):
                cursor.execute('INSERT INTO MatchDetails (MatchID, PlayerID, Score) VALUES (?, ?, ?)',
                               (match_id, player_id, score))
            conn.commit()

    @staticmethod
    def get_player_score():
        with sqlite3.connect(DatabaseAPI.DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT FirstName, OverScore FROM Players ORDER BY OverScore ASC')
            players = cursor.fetchall()
            return players

    @staticmethod
    def get_player_info(player_id):
        with sqlite3.connect(DatabaseAPI.DATABASE, uri=True) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Players WHERE PlayerID = ?', (player_id,))
            player_info = cursor.fetchone()

            if player_info:
                player_dict = {
                    'id': player_info[0],
                    'name': player_info[1],
                    'over_score': player_info[2],
                    'holes_play': player_info[3],
                    'wins': player_info[4]
                }
                return player_dict
            else:
                return None

    @staticmethod
    def get_player_matches():
        match_details = []

        with sqlite3.connect(DatabaseAPI.DATABASE, uri=True) as conn:
            cursor = conn.cursor()

            # SQL query to join Matches, MatchDetails, and Players tables
            query = '''
                SELECT Matches.MatchID, Matches.MatchDate, MatchDetails.PlayerID, MatchDetails.Score
                FROM MatchDetails
                LEFT JOIN Matches
                ON Matches.MatchID=MatchDetails.MatchID;
                '''

            cursor.execute(query)
            rows = cursor.fetchall()
            print("QUERY", rows)
            print("----------------------------")

            # Create a list
            curr_match_id = 1
            prev_player_id = 0

            temp_list = []
            for row in rows:
                match_id, match_date, player_id, score = row
                if curr_match_id != match_id:
                    match_details.append(temp_list)
                    temp_list = []
                    curr_match_id = match_id
                    prev_player_id = 0

                # Check for players not in match and add placeholder data
                print("GET Over: ", prev_player_id, player_id)
                if prev_player_id != player_id:

                    for i in range(prev_player_id + 1, player_id):
                        temp_list.append(match_id)
                        temp_list.append(match_date)
                        temp_list.append(i)
                        temp_list.append(' ')
                    prev_player_id = player_id
                temp_list.append(match_id)
                temp_list.append(match_date)
                temp_list.append(player_id)
                temp_list.append(score)
            match_details.append(temp_list)
        print(match_details)
        return match_details

    @staticmethod
    def get_specific_player_matches(player_id):
        with sqlite3.connect(DatabaseAPI.DATABASE, uri=True) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT Matches.MatchID, Matches.MatchDate, MatchDetails.Score FROM MatchDetails '
                           'LEFT JOIN Matches ON Matches.MatchID=MatchDetails.MatchID WHERE PlayerID = ?',
                           (player_id, ))
            rows = cursor.fetchall()
            print("SQL Specific: ", rows)
            print("----------------------------")
            match_details = []
            for row in rows:
                match_dict = {
                    'match_id': row[0],
                    'date': row[1],
                    'score': row[2]
                }
                match_details.append(match_dict)
            return match_details
