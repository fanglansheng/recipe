from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.forms import ModelForm, Textarea
from recipe.models import *
from mimetypes import guess_type
from django.forms import modelformset_factory


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
    #email = forms.EmailField(max_length=152,
    #                          label='Email',
    #                          widget=forms.TextInput(attrs={
    #                              'class': 'form-control',
    #                              'placeholder': 'Email'
    #                          }))
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
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    class Meta:
        model = User
        fields = ['username','password1', 'password2']

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.cleaned_data['password1'],
                                        )
        user.save()
        return user


class CreateWorkForm(forms.ModelForm): 
    class Meta:
        model = Work
        fields = ['bio', 'img']
        widgets = {
            'bio':Textarea(attrs={'form':"postform",
                                'maxlengt':"1000",
                                'placeholder':"What did you cook?"}),
        }
        error_css_class = 'error'
        required_css_class = 'required'
        error_messages={
            'bio':{
                'max_length':"Oops. You typed more than 1000 characters!",
            },
            'img':{
                'required':"At least post one picture!",
                'invalid':"Oops! The type is invalid.",
            },
        }

    def clean(self):
        cleaned_data = super(CreateWorkForm, self).clean()
        return cleaned_data

class CreateCommentForm(forms.ModelForm): 
    class Meta:
      model = WorkComments
      fields = ['content']

class recipeForm(forms.ModelForm):
    class Meta:
        model=Recipe
        exclude=('user','date',)
        widgets={'picture':forms.FileInput()}

class stepForm(forms.ModelForm):
    class Meta:
        model=Step
        exclude=('recipe',)
        widgets={'picture':forms.FileInput()}

