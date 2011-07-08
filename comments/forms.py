from django import forms
from django.contrib.comments.forms import CommentForm
from comments.models import AdexComment


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class AdexCommentForm(CommentForm):
    title = forms.CharField(max_length=300)
    image = forms.CharField(widget=forms.HiddenInput)

    def get_comment_model(self):
        return AdexComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(AdexCommentForm, self).get_comment_create_data()
        data['title'] = self.cleaned_data['title']
        data['image'] = self.cleaned_data['image']
        #data['name'] = self.cleaned_data['name_']
        #print data['image']
        #data['name'] = "herp"
        return data