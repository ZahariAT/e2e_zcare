from .client import Client


class Base:
    def __init__(self, client: Client, uuid: int, data: dict = None):
        self.client = client
        self.id = uuid
        if data:
            self._add_data(data)
        else:
            self.refresh()

    def _add_data(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)

    def refresh(self):
        raise NotImplemented


class Category(Base):
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def delete(self):
        endpoint = f'/api/categories/{self.id}/'
        self.client.delete(endpoint)

    def update(self, data):
        endpoint = f'/api/categories/{self.id}/'
        self.client.put(endpoint, data=data)
        self.refresh()

    def refresh(self):
        endpoint = f'/api/categories/{self.id}/'
        data = self.client.get(endpoint, json_response=True)
        self._add_data(data)


class Item(Base):
    def __init__(self, client: Client, uuid: int, data: dict = None):
        super().__init__(client, uuid, data)
        self.category = Category(self.client, self.category)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def delete(self):
        endpoint = f'/api/items/{self.id}/'
        self.client.delete(endpoint)

    def update(self, data):
        endpoint = f'/api/items/{self.id}/'
        self.client.put(endpoint, data=data)
        self.refresh()

    def refresh(self):
        endpoint = f'/api/items/{self.id}/'
        data = self.client.get(endpoint, json_response=True)
        self._add_data(data)


class Order(Base):
    def __init__(self, client: Client, data: dict):
        super().__init__(client, None, data)
        self.item = Item(self.client, self.item)

    def __str__(self):
        return f'item: {self.item}, total price: {self.total_price}, order date: {self.order_date}'

    def __repr__(self):
        return str(self)
