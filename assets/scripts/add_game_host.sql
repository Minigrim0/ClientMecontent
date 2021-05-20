-- Sets a user of a game to host
UPDATE userToGame SET is_host = true WHERE game_id = ? AND user_id = ?
