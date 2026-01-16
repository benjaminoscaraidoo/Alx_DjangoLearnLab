
from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """
    Query all books by a specific author
    """
    books = Book.objects.filter(author__name=author_name)

    print(f"Books by {author_name}:")
    for book in books:
        print(f"- {book.title}")


def list_all_books_in_library(library_name):
    """
    List all books in a library
    """
    library = Library.objects.get(name=library_name)

    # works for ManyToMany or reverse ForeignKey
    books = library.books.all()

    print(f"Books in library '{library_name}':")
    for book in books:
        print(f"- {book.title}")


def get_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library
    """
    library = Library.objects.get(name=library_name)
    librarian = library.librarian

    print(f"Librarian for '{library_name}':")
    print(f"- {librarian.name}")


if __name__ == "__main__":
    # sample calls
    query_books_by_author("George Orwell")
    list_all_books_in_library("Central Library")
    get_librarian_for_library("Central Library")
