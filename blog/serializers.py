from rest_framework import serializers
from .models import Category, User, Post,Comment,AuthorProfile,Tag,Bookmark,NewsletterSubscription

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class AuthorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AuthorProfile
        fields = ['id', 'user', 'bio', 'website', 'profile_picture']        

class CategorySerializer(serializers.ModelSerializer):
    posts=serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug','posts']  

class TagSerializer(serializers.ModelSerializer):
    posts=serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug','posts']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True, required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), source='tags', many=True, write_only=True, required=False)
    comments = serializers.StringRelatedField(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'author', 'category', 'category_id', 'tags', 'tag_ids', 'comments', 'created_at', 'updated_at', 'likes_count', 'is_liked', 'views_count']


    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class BookmarkSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post', write_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'post', 'post_id', 'created_at']

class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['id', 'email', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post', write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'body', 'post_id', 'created_at']