-- Starts a game, sets its end to now + {duration} seconds
UPDATE Game SET phase = 1, start_date = CURRENT_TIMESTAMP, end_date = datetime(CURRENT_TIMESTAMP, '+' || Game.game_duration || ' seconds') WHERE id = ?
