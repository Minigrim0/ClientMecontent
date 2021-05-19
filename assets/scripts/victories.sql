SELECT
    COUNT(*)
FROM
    (SELECT
        userToGame.user_id as winner_id
    FROM
        Game
    LEFT JOIN
        userToGame ON userToGame.game_id = Game.id AND userToGame.votes=(
        SELECT
            MAX(votes)
        FROM
            userToGame
        WHERE
            game_id=Game.id
        )
    WHERE
        Game.phase = 3
    )
WHERE
    winner_id = ?
