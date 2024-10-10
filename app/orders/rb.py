class RBOrder:
    def __init__(self, id: int | None = None,
                 status: str | None = None,
                 price: int | None = None,
                 user_id: int | None = None):
        self.id = id
        self.status = status
        self.price = price
        self.user_id = user_id

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'status': self.status, 'price': self.price, 'user_id': self.user_id}

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data