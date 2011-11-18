from django.db import models
from django.contrib.auth.models import User
from django import forms
from socialauth.models import Profile
from registration.forms import RegistrationFormUniqueEmail, attrs_dict

class RegistrationFormTest(RegistrationFormUniqueEmail):
    #first_name= forms.CharField(required=True)
    #last_name= forms.CharField(required=True)
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                         label=u'I have read and agree to the Terms of Service',
                         error_messages={'required': u"You must agree to the terms to register"})

class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            #self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    #email = forms.EmailField(label="Primary email",help_text='')
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
      model = Profile
      exclude = ('user',)

    def save(self, *args, **kwargs):
        u = self.instance.user
        #u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile