from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Answer by {self.author}'

class Flag(models.Model):
    CONTENT_CHOICES = [
        ('question', 'Question'),
        ('answer', 'Answer'),
    ]
    content_type = models.CharField(max_length=10, choices=CONTENT_CHOICES)
    object_id = models.PositiveIntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f'Flag on {self.content_type} #{self.object_id}'
