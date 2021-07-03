-- Returns every game ID that ends in less than 5 minutes
SELECT ID FROM Game WHERE phase = 1 AND CURRENT_TIMESTAMP - end_date < ?
