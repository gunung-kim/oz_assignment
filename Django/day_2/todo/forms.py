from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):

    class Meta:
        model=Todo
        fields=('title','description','start_date','end_date','is_completed')

class TodoCreate(TodoForm):

    class Meta(TodoForm.Meta):
        fields=TodoForm.Meta.fields+('end_date',)

# class TodoUpdate(forms.ModelForm):
#
#     class Meta:
#         model=Todo
#         fields=('title','description','start_date','end_date','is_completed')