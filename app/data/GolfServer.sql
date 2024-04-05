-- Create Players table
CREATE TABLE IF NOT EXISTS Players (
    PlayerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    OverScore INT DEFAULT 0,
    HolesPlay INT DEFAULT 0,
    Wins INT DEFAULT 0
);

-- Create Matches table
CREATE TABLE IF NOT EXISTS Matches (
    MatchID INTEGER PRIMARY KEY AUTOINCREMENT,
    MatchDate DATE DEFAULT CURRENT_DATE,
    WinnerID INT,
    FOREIGN KEY (WinnerID) REFERENCES Players(PlayerID)
);

-- Create MatchDetails table
CREATE TABLE IF NOT EXISTS MatchDetails (
    MatchDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
    MatchID INT,
    PlayerID INT,
    Score INT NOT NULL,
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID),
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
);
