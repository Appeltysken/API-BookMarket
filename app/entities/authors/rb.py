class RBAuthor:
    def __init__(self, id: int | None = None,
                 name: str | None = None,
                 bio: int | None = None,
                 author_picture: int | None = None):
        self.id = id
        self.name = name
        self.bio = bio
        self.author_picture = author_picture

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'name': self.name, 'bio': self.bio, 'author_picture': self.author_picture}

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data