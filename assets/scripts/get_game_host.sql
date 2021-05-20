-- Returns the id of the host of the game with the given ID
SELECT user_id FROM userToGame WHERE game_id = ? AND is_host = true
