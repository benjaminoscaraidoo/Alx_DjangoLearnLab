from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from relationship_app.models import Book, Library
from .models import Library
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def list_books(request):
    """
    Function-based view that lists all books with their authors
    """
    books = Book.objects.all()
    context = {'book_list': books} 
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
  """A class-based view for displaying details of a specific book."""
  model = Book
  template_name = 'relationship_app/library_detail.html'

  def get_context_data(self, **kwargs):
    """Injects additional context data specific to the book."""
    context = super().get_context_data(**kwargs)  # Get default context data
    book = self.get_object()  # Retrieve the current book instance
    context['average_rating'] = book.get_average_rating() 

class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class UserLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})