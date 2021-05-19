from discord import Embed

from src.decorators import needsDatabase

from DO.word import WordDO


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

        WordDO(word=word, user=user).save()

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
        return WordDO(word=word).delete()
