from discord import Embed


class ArtworkDO:
    """Represents the data of an artwork"""

    def __init__(self, artwork_title: str, artwork_url: str, user_id):
        self.user_id = user_id
        self.artwork_title = artwork_title
        self.artwork_url = artwork_url

    async def asEmbed(self, game_id: str, index: int, revealAuthor: bool = False):
        from singleton.client import Bot

        em = Embed(title=f"Participation #{index} (Partie #{game_id})")
        em.add_field(name="Titre de l'œuvre", value=self.artwork_title)

        print("Getting user :", self.user_id)
        user = await Bot.getInstance().fetch_user(int(self.user_id))
        print("User = ", user)
        author = user.username if revealAuthor else "XXXXXXXX"

        em.set_image(url=self.artwork_url)
        em.set_author(name=author)

        return em
