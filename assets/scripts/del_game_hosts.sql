-- Sets every user of a game to not host
UPDATE userToGame SET is_host = false WHERE game_id = ?
