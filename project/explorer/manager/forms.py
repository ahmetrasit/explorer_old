from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm
from django import forms
from .models import *
from django.db import models

class MainConfigurationForm(ModelForm):
    class Meta:
        model = MainConfiguration
        fields = ['team_name', 'intro_message', 'cpu_ratio', 'ram_ratio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'id':field,
                'rows':'1',
                'autocomplete':'none'
        })




class StepForm(ModelForm):
    raw_script = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Step
        fields = ['raw_script', 'short_name', 'description', 'no_of_outputs', 'sample_schema', 'access_list', 'status', 'special', 'created_for']



    def __init__(self, *args, **kwargs):
        advanced = ['no_of_outputs', 'sample_schema', 'status', 'special', 'created_for']
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            curr_class = 'form-control'
            if field in advanced:
                curr_class += ' advanced_mode'
            self.fields[field].widget.attrs.update({
                'class': curr_class,
                'id':field,
                'rows':'1',
                'autocomplete':'none'
        })


class MajorDataCategoryForm(ModelForm):
    class Meta:
        model = MajorDataCategory
        fields = ['category', 'description']


    def __init__(self, *args, **kwargs):
        widths = {'category':3, 'description':9}
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'id':field,
                'rows':'1',
                'autocomplete':'none'
        })


class AddUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username',  'password1', 'password2', 'email', 'role', 'special']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'id':field,
                'autocomplete':'none'
        })
