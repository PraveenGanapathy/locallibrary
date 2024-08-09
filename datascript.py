import subprocess
subprocess.check_call(['pip', 'install', 'requests'])
from catalog.models import Author, Book, Genre, BookInstance, Language
import random
import string
import requests
from datetime import date, timedelta

def create_author(first_name, last_name):
    date_of_birth = date.today() - timedelta(days=random.randint(365*20, 365*80))
    date_of_death = None
    if random.random() < 0.5:
        date_of_death = date_of_birth + timedelta(days=random.randint(365*20, 365*60))
    author = Author.objects.create(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        date_of_death=date_of_death
    )
    return author
# Define a function to create a language
def create_language(name):
    language, created = Language.objects.get_or_create(
        name=name
    )
    return language

# Define a function to create a book
def create_book(title, author, summary, isbn, genre, languages):
    book = Book.objects.create(
        title=title,
        author=author,
        summary=summary,
        isbn=isbn
    )
    book.save()  # Save the book instance
    book.genre.set([genre])
    #print(Book._meta.get_fields())
    for language in languages:
        book.languages.set([language])
    #print(book.__dict__)  # Print out the book object's attributes
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
genres = [
    "Science Fiction",
    "Fantasy",
    "Mystery",
    "Thriller",
    "Historical Fiction",
    "Romance",
    "Horror",
    "Biography",
    "Self-Help",
    "Graphic Novel",
    "Young Adult",
    "Adventure",
    "Dystopian",
    "Contemporary Fiction",
    "Crime",
    "Poetry",
    "Science",
    "Philosophy",
    "Non-Fiction",
    "Drama"
]
def check_details(title,first_name,last_name):
    if (
    first_name != last_name  # First name and last name are not the same
    and title != "Book"  # Title is not "Book"
    and first_name != "Author"  # First name is not "Author"
    and last_name != "Author"  # Last name is not "Author"
    and title != "unknown"  # Title is not "unknown"
    and first_name != "unknown"  # First name is not "unknown"
    and last_name != "unknown"  # Last name is not "unknown"
    ):
        return True
    else:
        return False

# Define a list of books to create
def extract_data(data):
    data = data.encode('utf-8').decode('utf-8')
    books = []
    for row in data.splitlines():
        columns = row.split(',')
        title = ''.join(e for e in columns[1] if e.isalpha() or e.isspace()).strip().capitalize()
        author = columns[2].strip()
        
        # Skip rows with empty title or author
        if not title or not author:
            continue
        
        # Skip rows with certain keywords
        keywords = ["Vol", "Volume", "&", "#"]
        if any(keyword in title for keyword in keywords):
            continue
        
        # Split authors by comma and filter out "Unknown"
        authors = [auth.strip() for auth in author.split(',') if "Unknown" not in auth]
        
        # If no authors left, skip this row
        if not authors:
            continue
        
        # Select one author randomly
        selected_author = random.choice(authors)
        
        # Split author name into first and last names
        author_names = selected_author.split()
        first_name = author_names[0].capitalize()
        last_name = ' '.join(author_names[1:]).capitalize()
        if check_details(title,first_name,last_name):
            summary = "A summary of " + title
            isbn = ''.join(random.choices(string.digits, k=13))
            genre = random.choice(genres)
            imprint = "Imprint " + str(random.randint(1, 100))
            due_back = "2024-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 28))
            status = random.choice(['a', 'o', 'm'])
            language = random.choice(["English", "Tamil", "Spanish", "French", "German", "Italian", "Portuguese", "Dutch", "Russian", "Chinese"])
            book = {
                "title": title,
                "first_name": first_name,
                "last_name": last_name,
                "summary": summary,
                "isbn": isbn,
                "genre": genre,
                "imprint": imprint,
                "due_back": due_back,
                "status": status,
                "language": language
            }
            books.append(book)
    return books

url = "https://gist.githubusercontent.com/apietrick24/bfffc6c0d47abf00029790381e89626d/raw/c7594d725856e13920fa2e2c159d3446e8bf159d/bookPublishingData.csv"
response = requests.get(url)
data = response.text

books = extract_data(data)

# Create the books
for book in books:
    if book["first_name"] and book["last_name"] and book["title"] and book["genre"]:
        author = create_author(book["first_name"], book["last_name"])
        genre, created = Genre.objects.get_or_create(name=book["genre"])
        language = create_language(book["language"])
        book_obj = create_book(
            book["title"],
            author,
            book["summary"],
            book["isbn"],
            genre,
            [language]
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