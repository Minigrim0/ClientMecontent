-- Returns the users that participate to a certain Game
SELECT Users.username as username, Users.discord_id FROM userToGame LEFT JOIN Users ON userToGame.user_id = Users.ID WHERE game_id = ?
