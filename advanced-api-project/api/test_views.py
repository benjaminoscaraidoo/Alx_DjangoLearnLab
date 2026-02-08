from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Author, Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        """Set up test data for all test cases."""
        self.client = APIClient()

        # Create a user for authenticated requests
        self.user = User.objects.create_user(username="tester", password="password123")

        # Create an author
        self.author = Author.objects.create(name="George Orwell")

        # Create books
        self.book1 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author
        )

    # ---------------------- READ (LIST + DETAIL) ----------------------

    def test_list_books(self):
        """Test retrieving a list of all books."""
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_single_book(self):
        """Test retrieving a single book by ID."""
        response = self.client.get(f"/api/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "1984")

    # ---------------------- CREATE (AUTH REQUIRED) ----------------------

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create a book."""
        data = {"title": "New Book", "publication_year": 2020, "author": self.author.id}
        response = self.client.post("/api/books/create/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Test that authenticated users can create a book."""
        self.client.login(username="tester", password="password123")
        data = {"title": "New Book", "publication_year": 2020, "author": self.author.id}
        response = self.client.post("/api/books/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # ---------------------- UPDATE (AUTH REQUIRED) ----------------------

    def test_update_book_authenticated(self):
        """Test updating a book."""
        self.client.login(username="tester", password="password123")
        update_data = {
            "title": "Updated 1984",
            "publication_year": 1949,
            "author": self.author.id
        }
        response = self.client.put(f"/api/books/update/?pk={self.book1.id}", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated 1984")

    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update a book."""
        update_data = {"title": "Blocked Update", "publication_year": 2000, "author": self.author.id}
        response = self.client.put(f"/api/books/update/?pk={self.book1.id}", update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------------------- DELETE (AUTH REQUIRED) ----------------------

    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete a book."""
        self.client.login(username="tester", password="password123")
        response = self.client.delete(f"/api/books/delete/?pk={self.book1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete a book."""
        response = self.client.delete(f"/api/books/delete/?pk={self.book1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------------------- FILTERING ----------------------

    def test_filter_books_by_publication_year(self):
        response = self.client.get("/api/books/?publication_year=1949")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "1984")

    # ---------------------- SEARCHING ----------------------

    def test_search_books_by_title(self):
        response = self.client.get("/api/books/?search=Farm")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Animal Farm")

    def test_search_books_by_author_name(self):
        response = self.client.get("/api/books/?search=orwell")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ---------------------- ORDERING ----------------------

    def test_order_books_by_title_desc(self):
        response = self.client.get("/api/books/?ordering=-title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Animal Farm")