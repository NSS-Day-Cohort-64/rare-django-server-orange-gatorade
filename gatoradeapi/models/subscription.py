from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class Subscription(models.Model):
    author = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="follower_relationships")
    follower = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="following_relationships")
    date_subscribed = models.DateTimeField(
        null=True, blank=True, auto_now=False, auto_now_add=True)
    date_unsubscribed = models.DateTimeField(
        null=True, blank=True, auto_now=False, auto_now_add=False)
    subscribed = models.BooleanField()

    class Meta:
        unique_together = ('author', 'follower')


# Connects the pre_save signal to the Subscription model
# Reciever decorator is a Django signal framework component used to attach a function(aka signal handler) to a specific signal, in this case pre_save
# Pre_save is a signal emitted just before a model's instance is saved to the database
# The sender of the pre_save signal is the Subscription model
@receiver(pre_save, sender=Subscription)
# Parameters are the model class, the instance of the model being saved, and any additonal KeyWordARGuments
def update_date_unsubscribed(sender, instance, **kwargs):
    # Check if the instance already has a primary key (it's an update)
    if instance.pk and instance.subscribed == False:
        # Sets the date_unsubscribed field of that Subscription instance to the current DateTime
        instance.date_unsubscribed = timezone.now()
