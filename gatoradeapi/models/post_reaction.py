from django.db import models

class PostReaction(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="reaction_relationships")
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="post_relationships")
    user = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="postreaction_relationships")
