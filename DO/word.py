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
        if self.id is None:
            db.update(script="add_word", params=(self.word, self.user))
        else:
            db.update(script="upd_word", params=(self.word, self.id))

    @needsDatabase
    def load(self, db):
        """Loads a word object from the database"""
        if self.id is None:
            raise Exception("Impossible de charger un mot sans son id !")

        # TODO: Handle SQLErrors
        data = db.fetch(script="get_word", params=(self.id,))
        print(data)

    @needsDatabase
    def delete(self, db):
        if self.word is None:
            raise Exception("Impossible de supprimer un mot sans sa valeur !")

        # TODO: Handle SQLErrors
        db.update(script="del_word", params=(self.word,))
        return True
