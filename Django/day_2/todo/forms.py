from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Todo, Comment


class TodoForm(forms.ModelForm):

    class Meta:
        model=Todo
        fields=('title','description','start_date','end_date','is_completed')
        widgets={
            "description": SummernoteWidget(),
            'title': forms.Textarea(attrs={'class': 'form-control',}),
            'start_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'end_date':forms.DateInput(attrs={'class':'form-control','type':'date'})
        }

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields=('completed_image',)
        widgets={
            'description': SummernoteWidget(),
            'title': forms.Textarea(attrs={'class': 'form-control',}),
            'start_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'end_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'is_completed':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'completed_image':forms.FileInput(attrs={'class':'form-control',}),
        }

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