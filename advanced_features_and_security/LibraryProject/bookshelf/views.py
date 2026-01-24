from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import SearchForm
from .forms import ExampleForm


@permission_required('content.can_view', raise_exception=True)
def book_list(request):
    books = book.objects.all()
    return render(request, 'content/article_list.html', {'books': books})

    form = SearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            books = books.filter(title__icontains=query)  # Prevents SQL injection

    return render(request, "bookshelf/book_list.html", {
        "form": form,
        "books": books
    })


@permission_required('content.can_create', raise_exception=True)
def article_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        Article.objects.create(title=title, body=body)
        return redirect('article_list')
    return render(request, 'content/article_create.html')


@permission_required('content.can_edit', raise_exception=True)
def article_edit(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        article.title = request.POST.get("title")
        article.body = request.POST.get("body")
        article.save()
        return redirect('article_list')
    return render(request, 'content/article_edit.html', {'article': article})


@permission_required('content.can_delete', raise_exception=True)
def article_delete(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return redirect('article_list')