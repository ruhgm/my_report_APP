from django import forms
from .models import Activity, Person
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity  # Replace with your actual Activity model
        fields = ['date', 'time_spent']  # Adjust the fields according to your model
    def clean_time_spent(self):
        time_spent = self.cleaned_data['time_spent']
        
        # Validate HH:MM format
        try:
            hours, minutes = map(int, time_spent.split(':'))
            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                raise ValidationError("Time must be between 00:00 and 23:59.")
        except ValueError:
            raise ValidationError("Invalid time format. Use HH:MM.")

        return time_spent

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person  # Replace with your actual Person model
        fields = ['name', 'info', 'location', 'phone_number', 'conversation_notes']
        widgets = {
            'next_appointment': forms.DateTimeInput(attrs={'type': 'datetime-local'})  # Adjust as needed
        }  
        # Adjust the fields according to your model
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User # Use User model here
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user