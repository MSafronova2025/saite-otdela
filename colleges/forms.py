from django import forms
from .models import College, NeedsRequest, RepairRequest, Request

class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = ['name', 'city', 'building_type', 'ownership_form', 'year_built']
        widgets = {
            'year_built': forms.NumberInput(attrs={'min': 1800, 'max': 2100}),
        }


class NeedsRequestForm(forms.ModelForm):
    class Meta:
        model = NeedsRequest
        fields = ['college', 'need_description', 'status']


class RepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ['college', 'repair_description', 'repair_status']

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
