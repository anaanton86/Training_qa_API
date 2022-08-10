from books.requests.api_clients import *
from random import randint

class TestApiClients:

    nr = randint(1, 9999999)
    clientName = 'Aaa'
    clientEmail = f'valid_email{nr}@email.com'
    response = login(clientName, clientEmail)

    def test_login_201(self):
        assert self.response.status_code == 201, "status code not ok"

    def test_login_has_token_key(self):
        assert 'accessToken' in self.response.json().keys(), "token key not present"

    def test_login_409(self):
        self.response = login(self.clientName, self.clientEmail)
        assert self.response.status_code == 409, "status code not ok"
        assert self.response.json()['error'] == "API client already registered. Try a different email.", "msg not ok"

    def test_invalid_email(self):
        self.response = login('Aaa', 'abc')
        assert self.response.status_code == 400, "status code not ok"
        assert self.response.json()['error'] == "Invalid or missing client email.", "msg not ok"

    def test_invalid_name(self):
        self.response = login('', 'abc@email.com')
        assert self.response.status_code == 400, "status code not ok"
        assert self.response.json()['error'] == "Invalid or missing client name.", "msg not ok"

