from django import forms
from .models import UserProfile, Payment


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'gender', 'dob', 'mobile', 'email',
            'id_proof_type', 'id_proof_number', 'vehicle_type', 'vehicle_name',
            'vehicle_number', 'rc_copy', 'id_proof_upload'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'id_proof_type': forms.Select(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        print("CLEANED DATA:", cleaned_data)  # Debugging output
        return cleaned_data
