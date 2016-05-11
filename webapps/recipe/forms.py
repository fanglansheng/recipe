from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm

from recipe.models import *

from mimetypes import guess_type


# Override AuthenticationForm and add more widgets
class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=152,
                              label='Username',
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Username',
                                  'html_name': 'login_username'
                              }))
    password = forms.CharField(max_length=20,
                              label='Password',
                              required=True,
                              widget=forms.PasswordInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Password',
                                  'html_name': 'login_password'
                              }))


# Override UserCreationForm and add more widgets
class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=152,
                              label='Username',
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Username'
                              }))
    email = forms.EmailField(max_length=152,
                              label='Email',
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Email'
                              }))
    password1 = forms.CharField(max_length=20,
                              label='Password',
                              widget=forms.PasswordInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Password'
                              }))
    password2 = forms.CharField(max_length=20,
                              label='Confirm Password',
                              widget=forms.PasswordInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Confirm Password'
                              }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.cleaned_data['password1'],
                                        email=self.cleaned_data['email'])
        user.save()
        return user


class CreateWorkForm(forms.ModelForm): 
    class Meta:
        model = Work
        fields = ['bio', 'img']
        # widgets = {
        #     'bio':Textarea(attrs={'form':"postform",
        #                         'class':"post-input",
        #                         'id': "post-text-area",
        #                         'maxlengt':"42",
        #                         'placeholder':"What "}),
        # }
        # error_messages={
        #     'text':{
        #         'required':"You should write something before post!",
        #         'max_length':"More than 42 words!",
        #     },
        #     'owner':{
        #         'required':"You should specify a user!",
        #     },
        # }

