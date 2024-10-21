class RBReview:
    def __init__(self, id: int | None = None,
                 text: str | None = None,
                 mark: int | None = None,
                 user_id: int | None = None,
                 book_id: int | None = None):
        self.id = id
        self.text = text
        self.mark = mark
        self.user_id = user_id
        self.book_id = book_id

    def to_dict(self) -> dict:
        data = {'id': self.id, 'text': self.text, 'mark': self.mark, 'user_id': self.user_id, 'book_id': self.book_id}

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data