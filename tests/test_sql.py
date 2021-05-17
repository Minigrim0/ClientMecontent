from decorators.connected import connected


def sample_user(db, cursor, scripts):
    cursor.execute(scripts["add_user"], ("Testuser", "discordID", 0))
    db.commit()
    return cursor.execute("SELECT last_insert_rowid() as id").fetchall()[0][0]


@connected
def test_addUser(db, cursor, scripts):
    assert sample_user(db, cursor, scripts) == 1


@connected
def test_getScore(db, cursor, scripts):
    user_id = sample_user(db, cursor, scripts)
    victories = cursor.execute(scripts["victories"], (user_id, )).fetchall()[0][0]
    assert victories == 0
    participations = cursor.execute(scripts["participations"], (user_id, )).fetchall()[0][0]
    assert participations == 0
