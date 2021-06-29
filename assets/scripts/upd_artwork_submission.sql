-- Sets the id of the Artwork to the userToGame table
UPDATE UserToGame SET artwork_id = ? WHERE user_id = ? and game_id = ?;
