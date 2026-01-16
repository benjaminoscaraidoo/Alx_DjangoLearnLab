from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """
    Query all books by a specific author
    """
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    return books


def list_all_books_in_library(library_name):
    """
    List all books in a library
    """
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    return books


def get_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library
    """
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    return librarian


if __name__ == "__main__":
    print(query_books_by_author("George Orwell"))
    print(list_all_books_in_library("Central Library"))
    print(get_librarian_for_library("Central Library"))
