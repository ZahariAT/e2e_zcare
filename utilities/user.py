import time

from .client import Client
from .item import Item, Order, Category


class User:
    def __init__(self, client: Client, refresh_timeout: int):
        self.client = client
        self._token = None
        self._refresh_token = None
        self._refresh_timeout = refresh_timeout * 60
        self._email = None
        self._password = None
        self._start_session = None

    def register(self, email: str, name: str, password: str, password2: str = None):
        endpoint = '/api/register/'
        data = {'email': email, 'name': name, 'password': password, 'password2': password2 if password2 else password}
        self.client.post(endpoint, data=data)

    def admin_login(self, username: str, password: str):
        endpoint = '/admin/login/'
        self.client.get(endpoint)
        data = {'username': username, 'password': password, 'csrfmiddlewaretoken': self.client.cookies['csrftoken']}
        self.client.post(endpoint, data=data)

    def api_login(self, email: str, password: str):
        endpoint = '/api/login/'
        data = {'email': email, 'password': password}
        r = self.client.post(endpoint, data=data, json_response=True)
        self._email = email
        self._password = password
        self._token = r['access_token']
        self._refresh_token = r['refresh_token']
        self.client.session.headers['Authorization'] = f'Bearer {self._token}'
        self._start_session = time.time()

    def _refresh_access_token(self):
        now = time.time()
        if now - self._start_session >= self._refresh_timeout - 10:
            endpoint = '/api/token/refresh/'
            data = {'refresh': self._refresh_token}
            res = self.client.post(endpoint, data=data, json_response=True)
            self._token = res['access']
            self.client.session.headers['Authorization'] = f'Bearer {self._token}'
            self._start_session = now

    def logout(self):
        endpoint = '/api/logout/'
        data = {'refresh_token': self._refresh_token}
        self.client.post(endpoint, data=data)
        self._token = None
        self._refresh_token = None
        self._email = None
        self._password = None
        self._start_session = None
        del self.client.session.headers['Authorization']

    def search_items(self, query: str):
        if self._token:
            self._refresh_access_token()
        endpoint = '/api/search/'
        items = self.client.get(endpoint, params={'q': query}, json_response=True)
        return [Item(self.client, item['id'], item) for item in items]

    def order_history(self, quantity: str = None, order_date_after: str = None):
        if self._token:
            self._refresh_access_token()
        endpoint = '/api/user/order_history'
        params = {'quantity': quantity, 'order_date_after': order_date_after}
        orders = self.client.get(endpoint, params=params, json_response=True)
        return [Order(self.client, order) for order in orders]

    def buy_item(self, item: Item, quantity: int):
        if self._token:
            self._refresh_access_token()
        endpoint = f'/api/items/{item.id}/buy'
        data = {'quantity': quantity}
        self.client.post(endpoint, data=data)
        item.refresh()
