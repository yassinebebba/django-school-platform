from management.models import Account
from .models import Student
from django import forms

class StudentAccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email',)


class StudentInfoUpdateForm(forms.ModelForm):
    notes = forms.CharField(label='Notes',
                            widget=forms.Textarea(attrs={'cols': '60', 'rows': '4'}),
                            required=False)

    class Meta:
        model = Student
        fields = ('phone_number', 'address_line_1', 'address_line_2', 'postcode',
                  'guardian_first_name', 'guardian_last_name', 'guardian_relationship', 'guardian_phone_number',
                  'notes')