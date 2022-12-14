from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from movies.models import (Movie,
                           Review,)


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Description',
                                  widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewAdminForm(forms.ModelForm):
    text = forms.CharField(label='Message',
                           widget=CKEditorUploadingWidget())

    class Meta:
        model = Review
        fields = '__all__'
