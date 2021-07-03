-- Returns all votes from a user
SELECT
    COUNT(*)
FROM
    Vote
WHERE artwork_id = (
    SELECT
        id
    FROM
        Artwork
    LEFT JOIN
        userToGame ON id = userToGame.artwork_id
    WHERE user_id = ? AND userToGame.game_id = ?
)
