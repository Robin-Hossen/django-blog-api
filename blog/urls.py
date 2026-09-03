from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookmarkViewSet, NewsletterSubscriptionViewSet, UserViewSet, AuthorProfileViewSet, CategoryViewSet, TagViewSet, PostViewSet, CommentViewSet


routers=DefaultRouter()# router object is created to automatically generate URL patterns for the viewsets.
# all the viewsets are registered with the router, which will handle the URL routing for each viewset.
routers.register(r'users',UserViewSet,basename='user')
routers.register(r'author-profiles',AuthorProfileViewSet,basename='author-profile')
routers.register(r'categories',CategoryViewSet,basename='category')
routers.register(r'tags',TagViewSet,basename='tag')
routers.register(r'posts',PostViewSet,basename='post')
routers.register(r'comments',CommentViewSet,basename='comment')
routers.register(r'bookmarks',BookmarkViewSet,basename='bookmark')
routers.register(r'newsletter-subscriptions',NewsletterSubscriptionViewSet,basename='newsletter-subscription')


urlpatterns = [
    path('',include(routers.urls)),# The router's URLs are included in the urlpatterns list
]