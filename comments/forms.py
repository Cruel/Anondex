from django import forms
from django.contrib.comments.forms import CommentForm
from comments.models import AdexComment
from medialibrary.models import LibraryFile


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class AdexCommentForm(CommentForm):
    file = forms.ModelChoiceField(LibraryFile.objects.all(), required=False)
    #is_anonymous = forms.BooleanField()

    def get_comment_model(self):
        return AdexComment

    def get_comment_create_data(self):
        data = super(AdexCommentForm, self).get_comment_create_data()
        data['file'] = self.cleaned_data['file']
        data['is_anonymous'] = self.data['user'] == 'anon'
        data['name'] = ''
        if self.data['user'] == 'temp':
            data['name'] = self.cleaned_data['name']
        return data