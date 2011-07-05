from django import forms
from django.contrib.comments.forms import CommentForm
from comments.models import AdexComment

class AdexCommentForm(CommentForm):
    title = forms.CharField(max_length=300)

    def get_comment_model(self):
        return AdexComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(AdexCommentForm, self).get_comment_create_data()
        data['title'] = self.cleaned_data['title']
        return data