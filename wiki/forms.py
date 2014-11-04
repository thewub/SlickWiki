from django import forms

from models import Revision

class EditForm(forms.ModelForm):
    class Meta:
        model = Revision
        fields = ['text', 'comment']