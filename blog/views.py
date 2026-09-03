




from rest_framework.decorators import action
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Bookmark, NewsletterSubscription, Post, Category, Tag, Comment, AuthorProfile, User
from .serializers import NewsletterSubscriptionSerializer, PostSerializer, CategorySerializer, TagSerializer, CommentSerializer, AuthorProfileSerializer, UserSerializer, BookmarkSerializer


from rest_framework.viewsets import ModelViewSet

# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.select_related('profile').all()
    serializer_class = UserSerializer

class AuthorProfileViewSet(ModelViewSet):
    queryset = AuthorProfile.objects.select_related('user').all()
    serializer_class = AuthorProfileSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]


    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'tags','author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def toggle_like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({'status': 'liked'}, status=status.HTTP_200_OK)

        return Response({'liked': liked, 'likes_count': post.likes.count()})



class BookmarkViewSet(ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('post', 'user')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NewsletterSubscriptionViewSet(ModelViewSet):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer
    permission_classes = [AllowAny]

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('post', 'user').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
