from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the post.
        # Note: This assumes that the object has an 'author' attribute for Post and a 'user' attribute for Comment.
        return getattr(obj, 'author', None) == request.user or getattr(obj, 'user', None) == request.user