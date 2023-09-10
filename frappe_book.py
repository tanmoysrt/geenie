import requests
from models import Book

# Class for querying frappe API ffor books
class FrappeBook:
  __instance = None
  endpoint = "https://frappe.io/api/method/frappe-library"

  def __new__(cls):
    if cls.__instance is None:
        cls.__instance = super().__new__(cls)
    return cls.__instance


  def get_books(self, page_no:int=1, search_type:str="", search_query:str=""):
    params = {
      "page": page_no,
    }
    if search_type != "" and search_query != "":
      params[search_type] = search_query
    response = requests.get(self.endpoint, params=params)
    if response.status_code == 200:
        res = response.json()
        return self.__books_from_json(res["message"])
    return []
  
  # Private methods
  def __books_from_json(self, books_json:list):
    books = []
    for book_json in books_json:
      tmp = Book(
        id=None,
        title=book_json["title"],
        authors=book_json["authors"],
        isbn=book_json["isbn"],
        publisher=book_json["publisher"],
        total_copies=0,
        available_copies=0,
        num_pages=book_json["  num_pages"],
        cover_image=self.__fetch_image_from_isbn(book_json["isbn"])
      )
      books.append(tmp)
    return books


  def __fetch_image_from_isbn(self, isbn:str) -> str:
    if isbn == "":
      return "/static/media/no-image.png"
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"