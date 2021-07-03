-- Returns every game ID where the vote ends in less than 5 minutes
SELECT ID FROM Game WHERE phase = 2 AND CURRENT_TIMESTAMP - (end_date + vote_duration) < ?
