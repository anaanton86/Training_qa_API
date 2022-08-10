from books.requests.books import *

class TestBooks:

    def test_get_books_200(self):
        r = get_books()
        assert r.status_code == 200, "status not ok"

    def test_get_all_books_total(self):
        r = get_books()
        assert len(r.json()) == 6, "book total not ok"

    def test_get_all_books_limit(self):
        r = get_books(limit=3)
        assert len(r.json()) == 3, "book limit not ok"

    def test_get_all_books_type_fiction(self):
        r = get_books(book_type='fiction')
        assert len(r.json()) == 4, "type fiction not ok"

    def test_get_all_books_type_nonfiction(self):
        r = get_books(book_type='non-fiction')
        assert len(r.json()) == 2, "type nonfiction not ok"

    def test_get_all_books_type_and_limit(self):
        r = get_books(book_type='fiction', limit=2)
        assert len(r.json()) == 2, "not ok"

    def test_get_books_invalid_type(self):
        r = get_books(book_type='abc')
        assert r.status_code == 400, "status code not ok"
        assert r.json()['error'] == "Invalid value for query parameter 'type'. Must be one of: fiction, non-fiction."

    def test_get_books_invalid_limit(self):
        r = get_books(limit=200)
        assert r.status_code == 400, "status code not ok"
        assert r.json()['error'] == "Invalid value for query parameter 'limit'. Cannot be greater than 20.", "wrong error"

    # def test_get_books_invalid_limit2(self):
    #     r = get_books(limit='abc')
    #     assert r.status_code == 400, "status code not ok"
    #     assert r.json()['error'] == "Invalid value for query parameter 'limit'. Must be numeric.", "wrong error"

    def test_get_books_invalid_limit3(self):
        r = get_books(limit=-1)
        assert r.status_code == 400, "status code not ok"
        assert r.json()['error'] == "Invalid value for query parameter 'limit'. Must be greater than 0.", "wrong error"

    def test_get_books_information(self):
        book = get_books().json()[0]
        expected_book = {
                            "id": 1,
                            "name": "The Russian",
                            "type": "fiction",
                            "available": True
                        }
        assert book == expected_book, "book info not ok"

    def test_get_book(self):
        r = get_book(1)
        expected = {
            "id": 1,
            "name": "The Russian",
            "author": "James Patterson and James O. Born",
            "isbn": "1780899475",
            "type": "fiction",
            "price": 12.98,
            "current-stock": 12,
            "available": True
        }
        assert r.status_code == 200, "status not ok"
        assert r.json() == expected, "book info not ok"

    def test_get_book_invalid_id(self):
        r = get_book(202)
        assert r.status_code == 404, "status not ok"
        assert r.json()['error'] == "No book with id 202", "wrong error"

    # def test_get_book_invalid_id2(self):
    #     r = get_book('abc')
    #     assert r.status_code == 404, "status not ok"
    #     assert r.json()['error'] == "Book id must be numeric", "wrong error"
