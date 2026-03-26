from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Todo,Comment


admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('message','completed_image')

@admin.register(Todo)
class TodoAdmin(SummernoteModelAdmin):
    list_display = ('title','start_date','end_date')
    list_filter = ('start_date','end_date')
    inlines = [CommentInline]


