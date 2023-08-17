from django.db import models

class Subscription(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="follower_relationships")
    follower = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="following_relationships")
    date_subscribed = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=True)
    date_unsubscribed = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)

    class Meta:
        unique_together = ('author', 'follower')

