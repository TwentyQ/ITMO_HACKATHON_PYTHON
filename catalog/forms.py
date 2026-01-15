from django import forms
from .models import Book, UserStatus


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'genre',
                  'description', 'cover_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1000,
                'max': 2100
            }),
            'genre': forms.Select(attrs={'class': 'form-control'}),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = UserStatus
        fields = ['reading_status']
        widgets = {
            'reading_status': forms.Select(attrs={'class': 'form-control'})
        }
