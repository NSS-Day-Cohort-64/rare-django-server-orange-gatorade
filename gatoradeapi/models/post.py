from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=55)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="created_posts")
    category = models.ForeignKey("Category", null=True, on_delete=models.SET_NULL, related_name="posts_of_category")
    publication_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=True)
    image_url = models.CharField(max_length=150)
    content = models.CharField(max_length=900)
    approved = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", through='PostTag')
    user_reactions = models.ManyToManyField("Reaction", through='PostReaction')
