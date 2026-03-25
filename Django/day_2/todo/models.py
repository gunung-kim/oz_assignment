from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
# from django.urls import reverse

User = get_user_model()

class Todo(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    is_completed = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('todo_detail',kwargs={'pk':self.pk})

    class Meta:
        verbose_name = "할일"
        verbose_name_plural = "할일 목록"

class Comment(models.Model):
    todo = models.ForeignKey(Todo,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} : {self.message} | {self.todo.title}"

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        ordering = ["-created_at"]
