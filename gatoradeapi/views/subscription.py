from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from gatoradeapi.models import Subscription
from gatoradeapi.models import Author



class SubscriptionViewSet(ViewSet):



    def list (self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def create(self, request):
            author = Author.objects.get(pk=request.data["author"])
            follower = Author.objects.get(pk=request.data["follower"])
            subscription = Subscription.objects.create(
                author=author,
                follower=follower
        )
       
            serializer = SubscriptionSerializer(subscription, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        subscription = Subscription.objects.get(pk=pk)
        subscription.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'author', 'follower', 'date_subscribed')

