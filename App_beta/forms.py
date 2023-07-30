from django import forms
from App_beta.models import *
from django.core.files.uploadedfile import InMemoryUploadedFile
from App_beta.humanize import naturalsize
from datetime import datetime, timedelta
from .models import Tool
from django.core.exceptions import ValidationError


# Create the form class.
class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'image'

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = Freelancer
        fields = []  # Picture is manual

class CreateProjectForm(forms.ModelForm):

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = Project
        fields = ['description','start_date','expected_end_date','pricing','tool']  # Picture is manual

class ApplyServiceForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
    #attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})) To be added in models.py
    pricing = forms.FloatField()
    tools = forms.ModelMultipleChoiceField(
        queryset = Tool.objects.all()
        )
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.now().date())
    delivery_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), initial=datetime.now().time())

    def clean(self):
        cleaned_data = super().clean()
        selected_date = cleaned_data.get('delivery_date')
        selected_time = cleaned_data.get('delivery_time')

        if selected_date and selected_time:
            selected_datetime = datetime.combine(selected_date, selected_time)
            min_datetime = datetime.now() + timedelta(hours=2)

            if selected_datetime <= min_datetime:
                self.add_error('delivery_time', "Please select a date and time at least 2 hours in the future.")