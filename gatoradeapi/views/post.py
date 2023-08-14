"""View module for handling requests about Posts"""
from django.db.models import Q
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
        if "approved" in request.query_params:
            post = post.filter(approved=True)
        if "author" in request.query_params:
            post = post.filter(author=request.query_params['author'][0])
        if "category" in request.query_params:
            post = post.filter(category=request.query_params['category'][0])
        # Handle filtering based on tags
        if "tag" in request.query_params:
            tag_ids = request.query_params.getlist('tag')
            q_objects = Q()
            for tag_id in tag_ids:
                q_objects |= Q(tags=tag_id)
            post = post.filter(q_objects)
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for a single Post

        Returns:
            Response -- JSON serialized Post
        """
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized Post instance
        """
        author = Author.objects.get(pk=request.data["author"])
        category = Category.objects.get(pk=request.data["category"])
        tags = Tag.objects.filter(pk__in=request.data["tags"])

        post = Post.objects.create(
            title=request.data['title'],
            author=author,
            category=category,
            image_url=request.data['image_url'],
            content=request.data['content'],
            approved=False,
        )

        post.tags.set(tags)

        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a Post

        Returns:
            Response -- Empty body with 204 status code
        """

        post = Post.objects.get(pk=pk)
        tags = Tag.objects.filter(pk__in=request.data["tags"])
        post.title = request.data["title"]
        post.author = Author.objects.get(pk=request.data["author"])
        post.category = Category.objects.get(pk=request.data["category"])
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.tags.set(tags)
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a Post

        Returns:
            Response -- Empty body with 204 status code
        """
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


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
    user_reactions = UserReactionSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'category', 'publication_date',
                  'image_url', 'content', 'approved', 'tags', 'user_reactions')
