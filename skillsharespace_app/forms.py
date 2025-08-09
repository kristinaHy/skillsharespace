from django import forms
from .models import Question, Answer,Flag

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']


class FlagForm(forms.ModelForm):
    class Meta:
        model = Flag
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }