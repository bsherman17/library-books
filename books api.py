import requests
import time
import csv

# List of popular authors
authors = [
    "Stephen King", "J.K. Rowling", "Agatha Christie", "C.S. Lewis", "J.R.R. Tolkien", 
    "George R.R. Martin", "Ernest Hemingway", "Mark Twain", "William Shakespeare", "Charles Dickens",
    "F. Scott Fitzgerald", "George Orwell", "Harper Lee", "Jane Austen", "Leo Tolstoy",
    "Margaret Atwood", "Virginia Woolf", "Roald Dahl", "Dan Brown", "J.D. Salinger",
    "John Steinbeck", "Jodi Picoult", "Nicholas Sparks", "Neil Gaiman", "Philip K. Dick"
]


# Open Library API
base_url = "http://openlibrary.org/search.json"

# Initialize list
books = []

# Loop through the authors
for author in authors:
    # max 100 books from author
    author_books = []
    while len(author_books) < 100:
        # query parameters
        params = {"author": author, "limit": 100, "page": len(author_books) // 100 + 1, "lang": "eng"}

        response = requests.get(base_url, params=params)

        # add books to list
        if response.status_code == 200:
            data = response.json()
            if "docs" in data:  
                author_books.extend(data["docs"])
            else:
                print(f"No books found for author {author}")
                break
        else:
            print(f"Failed to fetch books: {response.status_code}, {response.text}")

        # Sleep to avoid API limit
        time.sleep(1)

    # add books to list
    books.extend(author_books)

    # stop at enough books
    if len(books) >= 2500:
        break

# get the info and write to CSV file
with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Author", "First Published Year", "Subjects", "Cover Image URL"])
    for book in books:
        title = book.get('title')
        author = book.get('author_name', [None])[0] 
        first_published_year = book.get('first_publish_year')
        subjects = ", ".join(book.get('subject', [])[:1])
        cover_i = book.get('cover_i')
        cover_image_url = f"http://covers.openlibrary.org/b/id/{cover_i}-L.jpg" if cover_i else None
        writer.writerow([title, author, first_published_year, subjects, cover_image_url])
