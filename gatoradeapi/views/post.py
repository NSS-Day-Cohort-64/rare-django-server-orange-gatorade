"""View module for handling requests about Posts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gatoradeapi.models import Post, Author, Category, Tag, Reaction


class PostView(ViewSet):
    """Rare Post View"""

    def list(self, request):
        """Handle GET requests to get all Posts

        Returns:
            Response -- JSON serialized list of Posts
        """

        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('username', )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('label', )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('label', )


class UserReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('label', 'image_url')


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for Post"""

    author = AuthorSerializer(many=False)
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'category', 'publication_date',
                  'image_url', 'content', 'approved', 'tags', 'user_reactions')
