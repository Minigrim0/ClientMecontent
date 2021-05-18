from src.decorators import needsDatabase

from singleton.user import User


class Word:
    instance = None

    @staticmethod
    def getInstance():
        if Word.instance is None:
            Word()
        return Word.instance

    def __init__(self):
        if Word.instance is not None:
            raise Exception("This class is a singleton !")
        else:
            Word.instance = self

    @needsDatabase
    def addWord(self, word: str, user, db):
        user_id = User.getInstance().getUserID(str(user.id))
        db.update(script="add_word", params=(word, user_id))

    @needsDatabase
    def listWords(self, db):
        return db.fetch(script="list_words")

    @needsDatabase
    def delWord(self, word: str, db):
        exists = db.fetch(script="word_count", params=(word,))[0][0] == 1
        if exists:
            db.update(script="del_word", params=(word,))

        return exists
