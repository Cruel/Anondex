from comments.models import AdexComment
from comments.forms import AdexCommentForm

def get_model():
    return AdexComment

def get_form():
    return AdexCommentForm