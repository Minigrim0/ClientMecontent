from src.decorators import needsDatabase


class WordDO:
    def __init__(self, id=None, word=None, user=None):
        self.id = id
        self.word = word
        self.user = user

    @needsDatabase
    def save(self, db):
        """Saves the word object to the database"""
        if self.word is None or self.user is None:
            raise Exception("Les champs word et user ne peuvent pas être vide !")

        # TODO: Handle SQLErrors
        db.update(script="add_word", params=(self.word, self.user.id))

    @needsDatabase
    def load(self, db):
        """Loads a word object from the database"""
        if self.id is None and self.word is None:
            raise Exception("Impossible de charger un mot sans son id ni sa valeur !")

        # TODO: Handle SQLErrors
        id = self.id if self.id is not None else -1
        word = self.word if self.word is not None else ""
        self.id, self.word, self.user = db.fetch(script="get_word", params=(id, word))[0]

        return self

    @needsDatabase
    def delete(self, db):
        if self.word is None:
            raise Exception("Impossible de supprimer un mot sans sa valeur !")

        # TODO: Handle SQLErrors
        db.update(script="del_word", params=(self.word,))
        return True
