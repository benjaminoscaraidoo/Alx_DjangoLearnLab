from django.shortcuts import render
from django.http import HttpResponse
from relationship_app.models import Book


# Create your views here.
def list_books(request):
    """
    Function-based view that lists all books with their authors
    """
    books = Book.objects.all()

    #output = []
    #for book in books:
    #    output.append(f"{book.title} by {book.author}")

    context = {'book_list': books} 
    return render(request, 'relationship_app/list_books.html', context)