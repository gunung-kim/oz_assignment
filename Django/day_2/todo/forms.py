from django import forms
from .models import Todo, Comment


class TodoForm(forms.ModelForm):

    class Meta:
        model=Todo
        fields=('title','description','start_date','end_date','is_completed')

class TodoCreate(TodoForm):

    class Meta(TodoForm.Meta):
        fields=TodoForm.Meta.fields+('end_date',)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('message',)
        widgets={
            'message': forms.Textarea(
                attrs={'class': "form-control",
                       'rows':2,
                       "cols":70,
                       "placeholder":'내용없음',
                       })
        }
        label = {"message":"내용"}
