from django.forms import ModelForm
from .models import *

class MainConfigurationForm(ModelForm):
    class Meta:
        model = MainConfiguration
        fields = ['team_name', 'intro_message', 'cpu_ratio', 'ram_ratio', 'key_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'id':field,
                'rows':'1'
        })
