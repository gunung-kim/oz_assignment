from django.contrib import admin
from .models import Todo,Comment

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('message',)

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title','start_date','end_date')
    list_filter = ('start_date','end_date')
    inlines = [CommentInline]


