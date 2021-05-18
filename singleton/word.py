from src.decorators import needsDatabase

from singleton.user import User


class WordModel:
    instance = None

    @staticmethod
    def getInstance():
        if WordModel.instance is None:
            WordModel()
        return WordModel.instance

    def __init__(self):
        if WordModel.instance is not None:
            raise Exception("This class is a singleton !")
        else:
            WordModel.instance = self

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
