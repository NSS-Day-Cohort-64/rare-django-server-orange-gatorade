from django.db import models

class Comment(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="posted_comments")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=500)
    date_created = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=True)
