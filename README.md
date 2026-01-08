# Golf Server

A Flask-based web application for tracking golf matches, player statistics, and leaderboards. This application allows users to record match results, manage player profiles, and view comprehensive golf statistics.

## Features

- **Player Management** — Add and manage player profiles
- **Match Tracking** — Record match results with player scores
- **Leaderboard** — View overall player rankings and statistics
- **Player Statistics** — Track individual player performance including:
  - Overall score (par)
  - Total holes played
  - Score per hole average
  - Total match wins
- **Match History** — View detailed match history for each player
- **Responsive UI** — Bootstrap-based interface for desktop and mobile

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
- **JavaScript**: Vanilla JS for interactive elements

## Project Structure

```
golf_server/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── routes.py            # Application routes
│   └── templates/           # HTML templates
│       ├── layout.html      # Base template
│       ├── navbar.html      # Navigation bar
│       ├── index.html       # Player list & overview
│       ├── leaderboard.html # Leaderboard view
│       ├── player_detail.html # Individual player stats
│       ├── adddata.html     # Add match data form
│       └── addplayer.html   # Add player form
├── data/
│   ├── databaseApi.py       # Database operations
│   ├── GolfServer.db        # SQLite database
│   └── GolfServer.sql       # Database schema
├── run.py                   # Development server entry point
├── wsgi.py                  # Production WSGI entry point
└── requirements.txt         # Python dependencies
```

## Database Schema

The application uses three main tables:

### Players
- PlayerID (Primary Key)
- FirstName
- OverScore (cumulative score)
- HolesPlay (total holes played)
- Wins (match wins count)

### Matches
- MatchID (Primary Key)
- MatchDate
- WinnerID (Foreign Key to Players)

### MatchDetails
- MatchID (Foreign Key)
- PlayerID (Foreign Key)
- Score (score for this match)

## Installation

### Prerequisites
- Python 3.7+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/nickyhill/golf_server.git
cd golf_server
```

2. Install dependencies:
```bash
pip install flask
```

3. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Usage

### Adding a Player
1. Navigate to "Options" > "Add User"
2. Enter the player's name
3. Click "Add Player"

### Recording Match Data
1. Navigate to "Options" > "Add Data"
2. Select players who participated in the match
3. Enter each player's score
4. Enter holes played
5. Click "Submit"

The application will automatically:
- Calculate the match winner (lowest score)
- Update player statistics
- Record the match in history

### Viewing Statistics
- **Overview**: View leaderboard and all match data
- **Player Detail**: Click a player name to see individual statistics including:
  - Current score
  - Holes played
  - Average score per hole
  - Win count
  - Match history

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with player list |
| `/index` | GET | Redirect to home |
| `/overview` | GET | Leaderboard view |
| `/add_player` | GET, POST | Add new player |
| `/add_data` | GET, POST | Record match data |
| `/player/<player_id>` | GET | Individual player details |

## API Methods (DatabaseAPI)

### Players
- `get_players_name()` — Get all players
- `add_player(first_name)` — Add new player
- `get_player_info(player_id)` — Get player statistics

### Scores & Wins
- `get_player_score()` — Get leaderboard (sorted by score)
- `get_wins(player_id)` — Get player's win count
- `update_player_score(selected_players, scores, holes)` — Update player statistics

### Matches
- `add_data(selected_players, scores, holes_played)` — Record new match
- `get_player_matches()` — Get all match data
- `get_specific_player_matches(player_id)` — Get matches for specific player

## License

This project is open source and available under the MIT License.
