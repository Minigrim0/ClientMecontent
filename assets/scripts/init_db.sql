PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Users
(
    ID         INTEGER PRIMARY KEY,
    username   CHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS Game
(
    ID            INTEGER PRIMARY KEY AUTOINCREMENT,
    phase         INTEGER DEFAULT 0, -- Whether the users can register to participate or not
    start_date    TIMESTAMP,  -- The time the game started
    end_date      TIMESTAMP,  -- The time the game (should) end(ed)
    game_duration INTEGER,  -- The duration of the game
    vote_duration INTEGER DEFAULT 600,  -- The duration during which the users can vote
    nb_words      INTEGER DEFAULT 3  -- The number of words for the game
);

CREATE TABLE IF NOT EXISTS Words
(
    ID         INTEGER PRIMARY KEY AUTOINCREMENT,
    word       CHAR(255) UNIQUE NOT NULL,
    creator_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (creator_id) REFERENCES Users (ID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Artwork
(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    title CHAR(255),
    url CHAR(512)
);

CREATE TABLE IF NOT EXISTS Vote
(
    user_id    INTEGER NOT NULL,
    game_id    INTEGER NOT NULL,
    artwork_id INTEGER NOT NULL,  -- The artwork to user voted for
    CONSTRAINT fk_artwork FOREIGN KEY (artwork_id) REFERENCES Artwork (ID) ON DELETE CASCADE,
    CONSTRAINT fk_game FOREIGN KEY (game_id) REFERENCES Game (ID) ON DELETE CASCADE
    PRIMARY KEY (user_id, game_id)
);

CREATE TABLE IF NOT EXISTS userToGame
(
    user_id    INTEGER,
    game_id    INTEGER,
    votes      INTEGER,
    artwork_id INTEGER,  -- The url where the image has been posted
    is_host    BOOLEAN DEFAULT false,  -- Whether the user is host of the game or not (Can or cannot change parameters)
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES Users (ID) ON DELETE CASCADE,
    CONSTRAINT fk_game FOREIGN KEY (game_id) REFERENCES Game (ID) ON DELETE CASCADE,
    CONSTRAINT fk_artwork FOREIGN KEY (artwork_id) REFERENCES Artwork (ID) ON DELETE CASCADE,
    PRIMARY KEY (user_id, game_id)
);

CREATE TABLE IF NOT EXISTS wordToGame
(
    word_id INTEGER,
    game_id INTEGER,
    CONSTRAINT fk_word FOREIGN KEY (word_id) REFERENCES Words (ID) ON DELETE CASCADE,
    CONSTRAINT fk_game FOREIGN KEY (game_id) REFERENCES Game (ID) ON DELETE CASCADE,
    PRIMARY KEY (word_id, game_id)
);
