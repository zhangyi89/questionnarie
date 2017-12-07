from django import forms
from django.forms import ModelForm

from app01 import models


class QuestionnarieForm(forms.Form):
    title = forms.CharField(required=True, max_length=48)
    cls = forms.ChoiceField(choices=models.ClassList.objects.values_list('id', "title"))
    creator = forms.ChoiceField(choices=models.UserInfo.objects.values_list('id', "name"))


class QuestionForm(forms.Form):
    caption = forms.CharField(required=True, max_length=255, widget=forms.Textarea(attrs={
        'class': 'textarea', 'color': '#969696'
    }))
    # tp = forms.ChoiceField(choices=models.Question.objects.get)
    tp = forms.ChoiceField(choices=[(1, "打分"),
                                    (2, "单选"),
                                    (3, "评价"), ])


class QuestionModelForm(ModelForm):

    class Meta:
        model = models.Question
        fields = ['caption', 'tp']


class OptionModelForm(ModelForm):

    class Meta:
        model = models.Option
        fields = ['name', 'score']