from PIL import Image
from pathlib import Path
from io import BytesIO
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
    completed_image = models.ImageField(null=True, blank=True,upload_to='day_2/media/images/%Y/%m/%d')
    thumbnail = models.ImageField(null=True, blank=True,upload_to='day_2/media/images/%Y/%m/%d')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.completed_image:
            return super().save(*args, **kwargs)
        image = Image.open(self.completed_image)
        image.thumbnail((100,100))
        image_path = Path(self.completed_image.name)
        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix.lower()
        thumbnail_filename = f"{thumbnail_name}_thumb{thumbnail_extension}"
        if thumbnail_extension in ['.jpg','.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        else:
            return super().save(*args, **kwargs)
        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)
        self.thumbnail.save(thumbnail_filename,temp_thumb,save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)
    # def get_absolute_url(self):
    #     return reverse('todo_detail',kwargs={'pk':self.pk})

    def get_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return None

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
