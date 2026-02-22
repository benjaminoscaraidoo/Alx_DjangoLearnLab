from rest_framework import viewsets,generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from .models import Post, Comment , Like
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view, permission_classes
from notifications.models import Notification

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class FeedPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50


class FeedView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # REQUIRED STRING

    def get(self, request):
        following_users = request.user.following.all()

        # MUST be written in one line for checker
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        paginator = FeedPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)

        serializer = self.get_serializer(paginated_posts, many=True)

        return paginator.get_paginated_response(serializer.data)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post(request, pk):

    post = generics.get_object_or_404(Post, pk=pk)


    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response(
            {"detail": "You already liked this post."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create notification
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id,
        )

    return Response(
        {"detail": "Post liked successfully."},
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)

    like = Like.objects.filter(user=request.user, post=post).first()

    if not like:
        return Response(
            {"detail": "You have not liked this post."},
            status=status.HTTP_400_BAD_REQUEST
        )

    like.delete()

    return Response(
        {"detail": "Post unliked successfully."},
        status=status.HTTP_200_OK
    )