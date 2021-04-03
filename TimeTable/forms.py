from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserCreationModel, ScanTimeTableModel

class UserForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class':'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class':'form-control'}))
    email = forms.EmailField(max_length=50, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Id', 'class':'form-control'}))
    shortname = forms.CharField(max_length=5, required=True, help_text='Use short name used in Timetable', widget=forms.TextInput(attrs={'placeholder': 'Your Short Name(ABC)', 'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):

        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

class ScanTimeTableForm(forms.ModelForm):

    class Meta:
        model = ScanTimeTableModel
        fields = "__all__"
        widgets = {
            'division': forms.Select(attrs={'placeholder': 'Select Division', 'class':'custom-select'}),
            'semester': forms.Select(attrs={'placeholder': 'Select Semester', 'class':'custom-select'}),
            'year': forms.NumberInput(attrs={'placeholder': 'Select Year', 'class':'form-control'}),
            'image': forms.FileInput(attrs={'placeholder': 'Select Image', 'class':'form-control-file', 'id':'formFile'}),
        }

class SearchForm(forms.Form):

    CATAGORY_CHOICE=(
        ('1', 'Faculty Short Name'), 
        ('2', 'Division'), 
        ('3', 'Year'),
        ('4', 'Subject Name'),
    )
    catagory = forms.ChoiceField(required=True, choices=CATAGORY_CHOICE, widget=forms.Select(attrs={'placeholder': 'Select Category', 'class':'form-control'}))
    content = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Serach Data', 'class':'form-control'}))

class SigninForm(forms.Form):
    username = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class':'form-control'}))
    password = forms.CharField(required=True, max_length=150, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password', 'class':'form-control'}))

class SigninForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):

        super(SigninForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'