from django.db import models
from datetime import datetime
class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    is_completed = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
	    return self.title

    class Meta:
        verbose_name = "할일"
        verbose_name_plural = "할일 목록"

