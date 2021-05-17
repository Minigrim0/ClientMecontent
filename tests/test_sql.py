from decorators.connected import connected


def sample_user(db, cursor, scripts):
    cursor.execute(scripts["add_user"], ("Testuser", "discordID", 0))
    db.commit()
    return cursor.execute("SELECT last_insert_rowid() as id").fetchall()[0][0]


def sample_game(db, cursor, scripts):
    cursor.execute(scripts["create_game"], (10,))
    db.commit()
    return cursor.execute("SELECT last_insert_rowid() as id").fetchall()[0][0]


@connected
def test_addUser(db, cursor, scripts):
    assert sample_user(db, cursor, scripts) == 1


@connected
def test_getScore(db, cursor, scripts):
    user_id = sample_user(db, cursor, scripts)
    game_id = sample_game(db, cursor, scripts)

    assert cursor.execute(scripts["victories"], (user_id, )).fetchall()[0][0] == 0
    assert cursor.execute(scripts["participations"], (user_id, )).fetchall()[0][0] == 0

    cursor.execute(scripts["add_user_to_game"], (user_id, game_id, 0))
    db.commit()
    assert cursor.execute(scripts["participations"], (user_id, )).fetchall()[0][0] == 1
