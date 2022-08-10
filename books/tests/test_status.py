from books.requests.status import *

class TestStatus:

    def test_status_code_200(self):
        assert get_status().status_code == 200, "status code not ok"

    def test_status_body(self):
        assert get_status().json()['status'] == "OK", "satus msg not ok"