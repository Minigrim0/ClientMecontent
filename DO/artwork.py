class ArtworkDO:
    """Represents the data of an artwork"""

    def __init__(self, artwork_title: str, artwork_url: str, user_id):
        self.user_id = user_id
        self.artwork_title = artwork_title
        self.artwork_url = artwork_url
