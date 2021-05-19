-- Returns whether the user exists or not

SELECT
    CASE COUNT(*) 
        WHEN 1
            THEN true
        ELSE false
    END
FROM
    Users
WHERE
    id = ?
