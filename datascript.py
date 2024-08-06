import subprocess
subprocess.check_call(['pip', 'install', 'requests'])
from catalog.models import Author, Book, Genre, BookInstance, Language
import random
import random
import string
# Define a function to create an author
def create_author(first_name, last_name):
    author, created = Author.objects.get_or_create(
        first_name=first_name,
        last_name=last_name
    )
    return author

# Define a function to create a language
def create_language(name):
    language, created = Language.objects.get_or_create(
        name=name
    )
    return language

# Define a function to create a book
def create_book(title, author, summary, isbn, genre):
    book = Book.objects.create(
        title=title,
        author=author,
        summary=summary,
        isbn=isbn
    )
    book.genre.set([genre])
    return book

# Define a function to create a book instance
def create_book_instance(book, imprint, due_back, status):
    book_instance = BookInstance.objects.create(
        book=book,
        imprint=imprint,
        due_back=due_back,
        status=status
    )
    return book_instance

# Define a list of books to create
import random
import string

def extract_data(data):
    data = data.encode('utf-8').decode('utf-8')
    books = []
    for row in data.splitlines():
        columns = row.split(',')
        book = {
            "title": columns[1].strip('"').encode('utf-8').decode('utf-8'),
            "first_name": columns[2].split(',')[0].strip('"').encode('utf-8').decode('utf-8'),
            "last_name": columns[2].split(',')[-1].strip('"').encode('utf-8').decode('utf-8'),
            "summary": "A summary of " + columns[1].strip('"').encode('utf-8').decode('utf-8'),
            "isbn": ''.join(random.choices(string.digits, k=13)),
            "genre": columns[7].strip('"').encode('utf-8').decode('utf-8'),
            "imprint": "Imprint " + str(random.randint(1, 100)),
            "due_back": "2024-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 28)),
            "status": random.choice(['a', 'o', 'm'])
        }
        books.append(book)
    return books
import requests

url = "https://gist.githubusercontent.com/apietrick24/bfffc6c0d47abf00029790381e89626d/raw/c7594d725856e13920fa2e2c159d3446e8bf159d/bookPublishingData.csv"
response = requests.get(url)
data = response.text

books = extract_data(data)

# Create the books
for book in books:
    author = create_author(book["first_name"], book["last_name"])
    genre, created = Genre.objects.get_or_create(name=book["genre"])
    book_obj = create_book(
        book["title"],
        author,
        book["summary"],
        book["isbn"],
        genre
    )
    book_instance = create_book_instance(
        book_obj,
        book["imprint"],
        book["due_back"],
        book["status"]
    )

languages = [
    {"name": "English"},
    {"name": "Tamil"},
    {"name": "Spanish"},
    {"name": "French"},
    {"name": "German"},
    {"name": "Italian"},
    {"name": "Portuguese"},
    {"name": "Dutch"},
    {"name": "Russian"},
    {"name": "Chinese"},
]

for language in languages:
    Language.objects.get_or_create(name=language["name"])