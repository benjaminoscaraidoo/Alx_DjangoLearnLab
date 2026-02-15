from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
"""
Post Model
----------
Represents an individual blog post.

Fields:
    - title: The title of the blog post.
    - content: Main text body of the post.
    - published_date: Timestamp when the post was created.
    - author: ForeignKey to Django's User model.
"""

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    """
    Comment model for blog posts.
    Each comment is linked to a post and a user (author).
    """
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title[:20]}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    # New tagging field
    tags = TaggableManager()

    def __str__(self):
        return self.title