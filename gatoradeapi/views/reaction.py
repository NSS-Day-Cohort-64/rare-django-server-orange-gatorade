"""View module for handling requests about Reactions"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gatoradeapi.models import Reaction


class ReactionView(ViewSet):
    """Rare Reaction View"""

    def list(self, request):
        """Handle GET requests to get all Reactions

        Returns:
            Response -- JSON serialized list of Reactions
        """

        reaction = Reaction.objects.all()
        serializer = ReactionSerializer(reaction, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for a single Reaction

        Returns:
            Response -- JSON serialized Reaction
        """
        reaction = Reaction.objects.get(pk=pk)
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data)

    def create(self, request):
        """Handle Reaction operations

        Returns
            Response -- JSON serialized Reaction instance
        """

        reaction = Reaction.objects.create(
            label=request.data['label'],
            image_url=request.data['image_url']
        )

        serializer = ReactionSerializer(reaction)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a Reaction

        Returns:
            Response -- Empty body with 204 status code
        """

        reaction = Reaction.objects.get(pk=pk)
        reaction.label = request.data["label"]
        reaction.image_url = request.data["image_url"]
        reaction.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a Reaction

        Returns:
            Response -- Empty body with 204 status code
        """
        reaction = Reaction.objects.get(pk=pk)
        reaction.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for Reaction"""

    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
