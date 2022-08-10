import pytest

from books.requests.orders import *
from books.requests.api_clients import *

class TestOrders:

    def setup_method(self):
        self.token = get_token()
        self.token2 = get_token()

    # def teardown_method(self):
    #     print('am putea sa stergem user-ul din bd')

    def test_add_valid_order(self):
        r = add_order(self.token, 1, 'Anaa')
        assert r.status_code == 201, "status code not ok"
        assert r.json()['created'] is True, "order not created"
        #cleanup
        delete_order(self.token, r.json()['orderId'])

    def test_order_book_out_of_stock(self):
        r = add_order(self.token, 2, 'Aana')
        assert r.status_code == 404, "status code not ok"
        assert r.json()['error'] == "This book is not in stock. Try again later.", "msg not ok"

    def test_add_order_invalid_bookid(self):
        r = add_order(self.token, 88, 'Aa')
        assert r.status_code == 400, "status code not ok"
        # print (r.json())
        assert r.json()['error'] == "Invalid or missing bookId.", "msg not ok"

    @pytest.mark.skip
    def test_add_order_invalid_customer(self):
        r = add_order(self.token, 1, '')
        assert r.status_code == 201, "status code not ok"
        # print (r.json())
        assert r.json()['error'] == "Invalid or missing customerName.", "msg not ok"

    def test_get_orders(self):
        add1 = add_order(self.token, 1, 'Anaaa')
        add2 = add_order(self.token, 1, 'Anaaa')
        r = get_orders(self.token)
        assert r.status_code == 200, "status code not ok"
        assert len(r.json()) == 2, "get orders not working"
        #cleanup
        delete_order(self.token, add1.json()['orderId'])
        delete_order(self.token, add2.json()['orderId'])

    def test_get_order(self):
        # add
        id = add_order(self.token, 1, 'Anaa').json()['orderId']      # trivial bug orderId diferit de id
        # get
        r = get_order(self.token, id)
        assert r.status_code == 200, "status code not ok"
        assert r.json()['id'] == id, "id not ok"
        assert r.json()['bookId'] == 1, "book id not ok"
        assert r.json()['customerName'] == 'Anaa', "customer name not ok"
        assert r.json()['quantity'] == 1, "quantity not ok"
        #cleanup
        delete_order(self.token, id)

    def test_get_invalid_order_id(self):
        r = get_order(self.token, '123abc')
        assert r.status_code == 404, "status code not ok"
        assert r.json()['error'] == "No order with id 123abc.", "msg not ok"

    def test_get_order_invalid_token(self):
        r = get_order('123', '123abc')
        assert r.status_code == 401, "status code not ok"
        assert r.json()['error'] == "Invalid bearer token.", "msg not ok"

    def test_delete_order(self):
        # add
        add = add_order(self.token, 1, 'user1')
        # delete
        r = delete_order(self.token, add.json()['orderId'])
        assert r.status_code == 204, "status code not ok"
        #extra verif
        get_all = get_orders(self.token)
        assert len(get_all.json()) == 0, "order was not deleted"

    def test_delete_invalid_order_id(self):
        r = delete_order(self.token, '123abc')
        assert r.status_code == 404, "status code not ok"
        assert r.json()['error'] == "No order with id 123abc.", "msg not ok"

    def test_delete_order_unauth(self):
        id = add_order(self.token, 1, 'user1').json()['orderId']
        r = delete_order(self.token2, id)
        assert r.status_code == 404, "status code not ok"
        assert r.json()['error'] == f"No order with id {id}.", "msg not ok"
        # cleanup
        delete_order(self.token, id)

    def test_patch_valid_order_id(self):
        id = add_order(self.token, 1, 'Ana').json()['orderId']
        r = edit_order(self.token, id, 'Ana2')
        assert r.status_code == 204, "status code not ok"
        get = get_order(self.token, id)
        assert get.json()['customerName'] == 'Ana2', "update name not working"
        #cleanup
        delete_order(self.token, id)

    def test_patch_invalid_order_id(self):
        r = edit_order(self.token, '123abc', 'Ana2')
        assert r.status_code == 404, "status code not ok"
        assert r.json()['error'] == "No order with id 123abc.", "msg not ok"

    @pytest.mark.skip
    def test_patch_order_invalid_name(self):
        id = add_order(self.token, 1, 'Ana').json()['orderId']
        r = edit_order(self.token, id, '')
        assert r.status_code == 204, "status code not ok" # filetask. bug - pot edita empty string, msg 404
        get = get_order(self.token, id)
        assert get.json()['customerName'] == '', "update name not working"
        #cleanup
        delete_order(self.token, id)

























