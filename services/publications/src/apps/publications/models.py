from django.db import models

TYPE_CHOICES = (
    ('post', 'Publicación'),
    ('task', 'Tarea'),
)

class Publication(models.Model):
    community_id = models.IntegerField()
    user_id = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # TASK
    title = models.CharField(max_length=25, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)

class Submission(models.Model):
    task = models.ForeignKey(Publication, on_delete=models.CASCADE, limit_choices_to={'type': 'task'})
    user_id = models.IntegerField()
    file = models.FileField(upload_to="tasks/")
    submitted_at = models.DateTimeField()
    is_late = models.BooleanField()
    reviewed = models.BooleanField()
    grade = models.IntegerField(null=True, blank=True)

class Comment(models.Model):
    post = models.ForeignKey(Publication, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
