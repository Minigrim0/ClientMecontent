SELECT user_id FROM userToGame WHERE artwork_id = (SELECT artwork_id FROM Vote WHERE game_id = ? GROUP BY artwork_id ORDER BY COUNT(*) DESC LIMIT 1) and game_id = ?
