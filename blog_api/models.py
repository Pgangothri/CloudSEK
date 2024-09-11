from django.db import models

class BlogPost(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
