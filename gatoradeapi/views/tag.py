"""View module for handling requests about Tags"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gatoradeapi.models import Tag


class TagView(ViewSet):
    """Rare Tag View"""

    def list(self, request):
        """Handle GET requests to get all Tags

        Returns:
            Response -- JSON serialized list of Tags
        """

        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for a single Tag

        Returns:
            Response -- JSON serialized Tag
        """
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def create(self, request):
        """Handle Tag operations

        Returns
            Response -- JSON serialized Tag instance
        """

        tag = Tag.objects.create(
            label=request.data['label']
        )

        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a Tag

        Returns:
            Response -- Empty body with 204 status code
        """

        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]
        tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a Tag

        Returns:
            Response -- Empty body with 204 status code
        """
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for Tag"""

    class Meta:
        model = Tag
        fields = ('id', 'label', )
