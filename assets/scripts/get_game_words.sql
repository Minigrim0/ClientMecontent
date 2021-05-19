-- Returns all the words of the game with the given ID
SELECT Words.word FROM wordToGame LEFT JOIN Words ON Words.id = wordToGame.word_id WHERE game_id = ?
