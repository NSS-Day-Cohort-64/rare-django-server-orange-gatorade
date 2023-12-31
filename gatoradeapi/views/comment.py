from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from gatoradeapi.models import Comment, Author



class CommentViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)
  

    def list(self, request):

        comments = []
        comments = Comment.objects.all()
        post_id = request.query_params.get('post_id', None)
        if post_id is not None:
            comments = Comment.objects.filter(post_id=post_id)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
        




    def create(self, request):

        
        comment = Comment.objects.create(
            author = Author.objects.get(user=request.auth.user),
            post_id=request.data["post_id"],
            content=request.data["content"]
        )

        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.content = request.data["content"]
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name')

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False)
    
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post_id', 'content', 'date_created',)

       
        