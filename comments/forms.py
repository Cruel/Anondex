from django import forms
from django.contrib.comments.forms import CommentForm
from comments.models import AdexComment
from medialibrary.models import LibraryFile


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class AdexCommentForm(CommentForm):
    #title = forms.CharField(max_length=300)
    file = forms.ModelChoiceField(LibraryFile.objects.all(), required=False)

    def get_comment_model(self):
        return AdexComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(AdexCommentForm, self).get_comment_create_data()
        #data['title'] = self.cleaned_data['title']
        data['file'] = self.cleaned_data['file']
        #data['name'] = self.cleaned_data['name_']
        #print data['image']
        #data['name'] = "herp"
        return data