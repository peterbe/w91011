from django import forms
from django.contrib.auth.models import User
from utils.forms import BaseModelForm, BaseForm

class SignupForm(BaseModelForm):
    class Meta:
        model = User
        #exclude = ('password','username')
        fields = ('first_name','last_name','email')
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

class LoginForm(BaseForm):
    username_or_email = forms.CharField(label="Email address or username", max_length=200)
    password = forms.CharField(
      widget=forms.widgets.PasswordInput())

    def clean_username_or_email(self):
        value = self.cleaned_data['username_or_email']
        if User.objects.filter(email__iexact=value):
            pass
        elif User.objects.filter(username__iexact=value):
            pass
        else:
            raise forms.ValidationError("Not registered :(")
        return value

    def clean(self):
        data = super(LoginForm, self).clean()
        if 'username_or_email' in data and 'password' in data:
            value = data['username_or_email']
            if User.objects.filter(email__iexact=value):
                user = User.objects.get(email__iexact=value)
            elif User.objects.filter(username__iexact=value):
                user = User.objects.get(username__iexact=value)
            if not user.check_password(data['password']):
                raise forms.ValidationError("Not the right password. "\
              "Email us personally and we'll figure it out")
        return data