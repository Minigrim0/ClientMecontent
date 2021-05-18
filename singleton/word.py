from discord import Embed

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
        if len(word) > 255:
            raise Exception(f"Le mot ne peut pas être plus long que 255 caractères ! (Actuel : {len(word)})")

        user_id = User.getInstance().getUserID(str(user.id))
        db.update(script="add_word", params=(word, user_id))

    @needsDatabase
    def listWords(self, db):
        words = db.fetch(script="list_words")

        embed = Embed(title="Liste de mots", color=0xFF464A)
        for word, user in words:
            embed.add_field(name=word, value=user, inline=False)
        if len(words) == 0:
            embed.add_field(name="plutôt vide", value="meh", inline=False)

        return embed

    @needsDatabase
    def delWord(self, word: str, db):
        exists = db.fetch(script="word_count", params=(word,))[0][0] == 1
        if exists:
            db.update(script="del_word", params=(word,))

        return exists
