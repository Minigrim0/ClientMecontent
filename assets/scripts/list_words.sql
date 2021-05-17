-- Returns the list of the words with the author beside
SELECT word, users.username FROM Words LEFT JOIN Users ON Words.creator_id=Users.id
