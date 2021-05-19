import random
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

    def addWord(self, word: str, user):
        if len(word) > 255:
            raise Exception(f"Le mot ne peut pas être plus long que 255 caractères ! (Actuel : {len(word)})")

        WordDO(word=word, user=user).save()

    @needsDatabase
    def wordList(self, db):
        return db.fetch(script="list_words")

    def wordsEmbed(self):
        words = self.wordList

        embed = Embed(title="Liste de mots", color=0xFF464A)
        for word, user in words:
            embed.add_field(name=word, value=user, inline=False)
        if len(words) == 0:
            embed.add_field(name="plutôt vide", value="meh", inline=False)

        return embed

    def getRandomWords(self, nb_words: int):
        words = self.wordList()
        if nb_words > len(words):
            raise Exception(
                f"Il n'y a pas assez de mots dans la liste pour un tirage pareil !\
                    (Taille du tirage : {nb_words}; nombre de mots : {len(words)})"
            )

        chosen_words = []
        for x in range(nb_words):
            new_word = random.choice(words)
            chosen_words.append(WordDO(word=new_word[0]).load())
            del words[words.index(new_word)]

        return chosen_words

    def delWord(self, word: str):
        return WordDO(word=word).delete()
