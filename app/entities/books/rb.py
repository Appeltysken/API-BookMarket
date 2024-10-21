from decimal import Decimal

class RBBook:
    def __init__(self, id: int | None = None,
                 name: str | None = None,
                 author_id: int | None = None,
                 genre: str | None = None,
                 publisher: str | None = None,
                 description: str | None = None,
                 price: Decimal | None = None,
                 book_picture: str | None = None,
                 user_id: int | None = None):
        
        self.id = id
        self.name = name
        self.author_id = author_id
        self.genre = genre
        self.publisher = publisher
        self.description = description
        self.price = price
        self.book_picture = book_picture
        self.user_id = user_id
        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'name': self.name, 'author_id': self.author_id, 'genre': self.genre, 'publisher': self.publisher, 'description': self.description,
                'price': self.price, 'book_picture': self.book_picture, 'user_id': self.user_id}

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data