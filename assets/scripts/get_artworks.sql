-- Returns the artworks relative to the game with the given ID
SELECT title, url, userToGame.user_id FROM Artwork LEFT JOIN userToGame on ID = userToGame.artwork_id WHERE userToGame.game_id = ?
