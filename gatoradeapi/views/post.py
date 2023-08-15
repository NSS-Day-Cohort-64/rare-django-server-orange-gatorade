"""View module for handling requests about Posts"""
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
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

        post = Post.objects.all().order_by('-id')
        if "user" in request.query_params:
            post = post.filter(author__user=request.auth.user)
        if "approved" in request.query_params:
            post = post.filter(approved=True)
        if "author" in request.query_params:
            post = post.filter(author=request.query_params['author'][0])
        if "category" in request.query_params:
            post = post.filter(category=request.query_params['category'][0])
        # Handle filtering based on tags
        if "tag" in request.query_params:
            # Get a list of all tag ids from the query parameters
            tag_ids = request.query_params.getlist('tag')
            # Create an empty Q object to build dynamic queries
            q_objects = Q()
            # Iterate through each tag ID and create an OR condition with Q
            for tag_id in tag_ids:
                # Adds the current tags query to q_objects using the OR clause
                # Effectively builds a query like: q_objects = 1 OR 2 OR 3 as the loop iterates
                q_objects |= Q(tags=tag_id)
            # Filter the post based on the intricate q_objects query
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
        author = Author.objects.get(user=request.auth.user)
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

    # Declares token_key and initializes it with the SerializerMethodField
    # Said class takes a method in the for of get_{field_name}
    # token_key = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('id', 'username',)

    # This is the method being called above
    #def get_token_key(self, author):
        #try:
            # Here it finds the Token with a user value equal to the author.user value
            #token = Token.objects.get(user=author.user)
            # Then it returns the key
            #return token.key
        #except Token.DoesNotExist:
            #return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label', )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label', )


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
