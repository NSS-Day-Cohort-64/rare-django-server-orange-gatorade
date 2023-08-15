
from gatoradeapi.models import Author
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status




class AuthorViewSet(ViewSet):

    def list(self, request):
        authors = []
        authors = Author.objects.all()

        if request.query_params.get('is_active') is not None:
            if request.query_params.get('is_active') == 'true':
                authors = authors.filter(user__is_active=True)
            elif request.query_params.get('is_active') == 'false':
                authors = authors.filter(user__is_active=False)
        if request.query_params.get('is_staff') is not None:
            if request.query_params.get('is_staff') == 'true':
                authors = authors.filter(user__is_staff=True)
            elif request.query_params.get('is_staff') == 'false':
                authors = authors.filter(user__is_staff=False)
        
        if "current" in request.query_params:
            authors = authors.filter(user=request.auth.user)

        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
         
        author = Author.objects.get(pk=pk)
        user = author.user  
        author.delete()
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        author = Author.objects.get(pk=pk)
        author.user.first_name = request.data["first_name"]
        author.user.last_name = request.data["last_name"]
        author.user.username = request.data["username"]
        author.user.save()
        author.bio = request.data["bio"]
        author.profile_image_url = request.data["profile_image_url"]
        author.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('username', 'first_name', 'last_name',)


class AuthorSerializer(serializers.ModelSerializer):

    followed_authors = SubscriptionSerializer(many=True)
    followers = SubscriptionSerializer(many=True)
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'username', 'created_on', 'is_staff', 'is_active',  'bio', 'profile_image_url', 'followed_authors', 'followers')


     


