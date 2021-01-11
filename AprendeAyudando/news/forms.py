from django import forms
from .models import News
from django.forms import Textarea

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['headline', 'content']
        widgets = {
            'headline': forms.TextInput(attrs={'class':'form-control'}),
            'content': Textarea(attrs={'class':'form-control'})
        }