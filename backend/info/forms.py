from django.forms import ModelForm
from django.forms.widgets import TextInput
from .models import Genre

class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
