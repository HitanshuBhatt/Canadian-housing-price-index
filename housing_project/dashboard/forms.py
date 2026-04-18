from django import forms
from django.contrib.auth.models import User


# form used to upload csv file
class CSVUploadForm(forms.Form):
    # input field to select file
    csv_file = forms.FileField(label="Upload a CSV file")

    # validation for uploaded file
    def clean_csv_file(self):
        # get uploaded file from cleaned form data
        csv_file = self.cleaned_data["csv_file"]

        # check if it is a .csv file
        if not csv_file.name.lower().endswith(".csv"):
            raise forms.ValidationError("Please upload a valid CSV file.")

        # check if file contains data and is not empty by checking size
        if csv_file.size == 0:
            raise forms.ValidationError("The uploaded file is empty.")

        # return the validated file
        return csv_file


# login form for email and password
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email address")
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )


# signup form for new account
class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=150, label="First name")
    last_name = forms.CharField(max_length=150, label="Last name")
    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={"type": "date"})
    )
    email = forms.EmailField(label="Email address")
    password = forms.CharField(
        label="Password",
        min_length=8,
        widget=forms.PasswordInput,
        help_text="Password must be at least 8 characters."
    )

    # check if email already exists
    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        return email