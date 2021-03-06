from django import forms

from wiki.models import Revision

class EditForm(forms.ModelForm):
    class Meta:
        model = Revision
        fields = ['text', 'comment']
        widgets = {
            'text' : forms.Textarea(attrs={'cols': 40, 'rows': 15, 'autofocus': 'true'})
        }
        labels = {
            'text' : ''
        }