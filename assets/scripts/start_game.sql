-- Starts a game, sets its end to now + {duration} seconds
UPDATE Game SET registration_phase = false, start_date = CURRENT_TIMESTAMP, end_date = datetime(CURRENT_TIMESTAMP, '+' || Game.duration || ' seconds') WHERE id = ?
