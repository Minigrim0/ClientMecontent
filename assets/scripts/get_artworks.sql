-- Returns the artworks relative to the game with the given ID
SELECT Artwork.title, Artwork.url, user_id FROM UserToGame LEFT JOIN Artwork ON artwork_id = Artwork.ID WHERE game_id = ?
